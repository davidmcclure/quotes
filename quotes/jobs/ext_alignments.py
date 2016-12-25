

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

        """
        Create N empty partition lists.
        """

        return super().__init__([] for _ in range(size))

    def add_task(self, task):

        """
        Add a task to the partition with the lowest count.
        """

        counts = [sum([t.count for t in p]) for p in self]

        self[np.argmin(counts)].append(task)

    def make_args(self):

        """
        Convert into {record_id: int, year: int} args.
        """

        return [
            [dict(novel_id=t.novel_id, year=t.year) for t in p]
            for p in self
        ]


class Tasks:

    def __init__(self, years=10):

        """
        Build a set of (Chadwyck novel id, year, BPO article count) tuples for
        each of the N years after the publicaton of each novel.
        """

        self.tasks = []

        for novel in ChadhNovel.query.all():
            for year in range(novel.year, novel.year+years+1):

                # Count BPO articles in the year
                count = (
                    BPOArticle.query
                    .filter_by(year=year)
                    .count()
                )

                self.tasks.append(Task(novel.id, year, count))

    def sorted_tasks(self):

        """
        Sort tasks by count, descending.
        """

        return sorted(
            self.tasks,
            key=lambda t: t.count,
            reverse=True,
        )

    def partitions(self, size: int):

        """
        Split the tasks into N partitions, each with approximately the same
        total number of alignment tasks.
        """

        partitions = Partitions(size)

        for task in self.tasks:
            partitions.add_task(task)

        return partitions.make_args()


class ExtAlignments(Scatter):

    def __init__(self, result_dir: str):

        """
        Set the input paths.
        """

        self.result_dir = result_dir

        self.matches = []

    def args(self):

        """
        Generate (novel id, year) pairs.
        """

        return ChadhNovel.alignment_pairs()

    def partitions(self, size: int):

        """
        Spit novel + year alignment tasks into partitions that roughly balance
        the total number of alignments for each rank.
        """

        tasks = Tasks()

        return tasks.partitions(size)

    def process(self, novel_id: str, year: int):

        """
        Query BPO texts in a given year against a novel.
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

            if i % 1000 == 0:
                print('align', dt.now().isoformat(), i, mem_pct())

        # Flush results when >1k.
        if len(self.matches) > 1000:
            self.flush()

    def flush(self):

        """
        Flush the matches to disk, clear cache.
        """

        path = os.path.join(
            self.result_dir,
            '{}.json'.format(str(uuid.uuid4())),
        )

        with open(path, 'w') as fh:
            ujson.dump(self.matches, fh)

        self.matches.clear()
