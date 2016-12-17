

import os

from quotes.utils import scan_paths

from .scatter import Scatter


class UnzipBPO(Scatter):

    def __init__(self, corpus_dir: str):

        """
        Set the input paths.
        """

        self.corpus_dir = corpus_dir

    def args(self):

        """
        Generate BPO archive paths.
        """

        pass

    def process(self, path: str):

        """
        Unzip the archive into a new directory.
        """

        pass
