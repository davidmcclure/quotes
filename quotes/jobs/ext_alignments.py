

import os
import ujson
import uuid

import numpy as np

from datetime import datetime as dt
from collections import namedtuple

from quotes.text import Text
from quotes.models import ChadhNovel, BPOArticle
from quotes.utils import mem_pct

from .scatter import Scatter


Task = namedtuple('Task', [
    'novel_id',
    'year',
    'count',
])


class Partitions(list):

    def __init__(self, size: int):
        """Create N empty partition lists.

        Args:
            size (int): The MPI size.
        """
        return super().__init__([] for _ in range(size))

    def counts(self):
        """Get the total alignment counts for each partition.

        Returns: int
        """
        return [sum([t.count for t in p]) for p in self]

    def add_task(self, task):
        """Add a task to the partition with the lowest count.

        Args:
            task (Task)
        """
        self[np.argmin(self.counts())].append(task)

    def make_args(self):
        """Convert into MPI task args.

        Returns: list of dict(novel_id=int, year=int)
        """
        return [
            [dict(novel_id=t.novel_id, year=t.year) for t in p]
            for p in self
        ]


class Tasks:

    @classmethod
    def from_chadh(cls, years=10):
        """Build a set of (Chadwyck novel id, year, BPO article count) tuples
        for each of the N years after the publicaton of each novel.

        Args:
            years (int): Take this many years after the publication date.
        """
        tasks = []

        for novel in ChadhNovel.query.all():
            for year in range(novel.year, novel.year+years+1):

                # Count BPO articles in the year.
                count = (
                    BPOArticle.query
                    .filter_by(year=year)
                    .count()
                )

                tasks.append(Task(novel.id, year, count))

        return cls(tasks)

    def __init__(self, tasks):
        """Set the list of tasks.

        Args:
            tasks (list of Task)
        """
        self.tasks = tasks

    def sorted_tasks(self):
        """Sort tasks by count, descending.

        Returns: list of Task
        """
        return sorted(
            self.tasks,
            key=lambda t: t.count,
            reverse=True,
        )

    def partitions(self, size: int):
        """Split the tasks into N partitions, each with approximately the same
        total number of alignment tasks.

        Args:
            size (int): MPI size.
        """
        partitions = Partitions(size)

        for task in self.tasks:
            partitions.add_task(task)

        return partitions


class ExtAlignments(Scatter):

    def __init__(self, result_dir: str):
        """Set the input paths.

        Args:
            result_dir (str): Dump results to this directory.
        """
        self.result_dir = result_dir

        self.matches = []

    def partitions(self, size: int):
        """Spit novel + year alignment tasks into partitions that roughly
        balance the total number of alignments for each rank.

        Args:
            size (int): MPI size.
        """
        tasks = Tasks.from_chadh()

        partitions = tasks.partitions(size)

        # Eyeball the alignment totals.
        print(partitions.counts())

        return partitions.make_args()

    def process(self, novel_id: int, year: int):
        """Query BPO texts in a given year against a novel.

        Args:
            novel_id (int): Chadwyck Healey novel id.
            year (int): Align with BPO articles in this year.
        """
        # Hydrate the Chadwyck novel.
        novel = ChadhNovel.query.get(novel_id)
        a = Text(novel.text)

        # Query BPO articles in the year.
        articles = BPOArticle.query.filter_by(year=year)

        for i, article in enumerate(articles):

            try:

                b = Text(article.text)

                # Align article -> novel.
                matches = a.match(b)

                # Record matches.
                for m in matches:

                    a_prefix, a_snippet, a_suffix = a.snippet(m.a, m.size)
                    b_prefix, b_snippet, b_suffix = b.snippet(m.b, m.size)

                    self.matches.append(dict(

                        a_id=novel.id,
                        b_id=article.record_id,

                        a_start=m.a,
                        b_start=m.b,
                        size=m.size,

                        a_prefix=a_prefix,
                        a_snippet=a_snippet,
                        a_suffix=a_suffix,

                        b_prefix=b_prefix,
                        b_snippet=b_snippet,
                        b_suffix=b_suffix,

                    ))

            except Exception as e:
                print(e)

            # TODO|dev
            # if i % 1000 == 0:
            print('align', i, mem_pct(), dt.now().isoformat())

        # Flush results when >1k.
        if len(self.matches) > 1000:
            self.flush()

    def flush(self):
        """Flush the matches to disk, clear cache.
        """
        path = os.path.join(
            self.result_dir,
            '{}.json'.format(str(uuid.uuid4())),
        )

        with open(path, 'w') as fh:
            ujson.dump(self.matches, fh)

        self.matches.clear()
