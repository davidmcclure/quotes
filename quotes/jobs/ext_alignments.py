

import os
import ujson
import uuid

import numpy as np

from datetime import datetime as dt
from collections import namedtuple
from boltons import iterutils

from quotes.text import Text
from quotes.models import ChadhNovel, QueryText, BPOArticle
from quotes.utils import mem_pct

from .scatter import Scatter


class ExtAlignments(Scatter):

    def __init__(self, query_slug: str, result_dir: str):
        """Set the input paths.

        Args:
            query_slug (str): Query against this text.
            result_dir (str): Dump results to this directory.
        """
        self.query_text = QueryText.query.filter_by(slug=query_slug).one()

        self.a = Text(self.query_text.text)

        self.result_dir = result_dir

        self.matches = []

        self.counter = 0

    def args(self):
        """Hydrate the full list of BPO ids.

        Returns: list of int
        """
        return iterutils.chunked(BPOArticle.record_ids(), 1000)

    def process(self, record_ids):
        """Query BPO texts in a given year against a novel.

        Args:
            novel_id (int): Chadwyck Healey novel id.
            year (int): Align with BPO articles in this year.
        """
        # Hydrate the article partition.
        articles = BPOArticle.load_partition(record_ids)

        for article in articles:

            try:

                b = Text(article.text)

                # Align article -> text.
                matches = self.a.match(b)

                # Record matches.
                for m in matches:

                    a_prefix, a_snippet, a_suffix = self.a.snippet(m.a, m.size)
                    b_prefix, b_snippet, b_suffix = b.snippet(m.b, m.size)

                    self.matches.append(dict(

                        a_id=self.query_text.id,
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

            self.counter += 1

            if self.counter % 1000 == 0:
                print(
                    'align',
                    self.rank,
                    self.counter,
                    mem_pct(),
                    dt.now().isoformat(),
                )

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
