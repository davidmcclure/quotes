

import numpy as np
import json

from quotes.utils import mem_pct


class Scatter:

    def args(self):
        raise NotImplementedError

    def process(self, arg):
        raise NotImplementedError

    def flush(self):
        raise NotImplementedError

    def __call__(self):

        """
        Dump year -> token -> offset -> count.
        """

        from mpi4py import MPI

        comm = MPI.COMM_WORLD

        size = comm.Get_size()
        rank = comm.Get_rank()

        # ** Scatter JSON-encoded segments.

        segments = None

        if rank == 0:

            segments = [
                json.dumps(list(s))
                for s in np.array_split(list(self.args()), size)
            ]

        segment = comm.scatter(segments, root=0)

        args = json.loads(segment)

        print(rank, len(args))

        ## ** Gather offsets, flush.

        for i, arg in enumerate(args):

            try:

                if type(arg) is dict:
                    self.process(**arg)

                else:
                    self.process(arg)

            except Exception as e:
                print(e)

            if i%100 == 0:
                print(rank, i, mem_pct())

        self.flush()
