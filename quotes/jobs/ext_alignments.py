

import os

from quotes.text import Text
from quotes.models import ChadhNovel, BPOArticle

from .scatter import Scatter


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

        return []

    def process(self, novel_id: str, year: int):

        """
        Query BPO texts in a given year against a novel.
        """

        # Read the Chadwyck novel.

        fname = '{}.txt'.format(slug)

        novel_path = os.path.join(self.corpus_dir, fname)

        novel = Text.from_chadh_c19(novel_path)

        # Query BPO articles in the year.

        articles = BPOArticle.query.filter_by(year=year)

        for article in articles:

            bpo_text = Text(article.full_text)

            # Align article -> novel.
            matches = novel.match(bpo_text)

            # Record matches.
            for m in matches:

                a_prefix, a_snippet, a_suffix = novel.snippet(m.a, m.size)
                b_prefix, b_snippet, b_suffix = bpo_text.snippet(m.b, m.size)

                self.matches.append(dict(

                    chadh_slug=novel.metadata['slug'],
                    bpo_record_id=article.record_id,

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

        # TODO: flush matches when >1k
