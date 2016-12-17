

import os

from quotes.text import Text
from quotes.chadh_corpus import ChadhCorpus
from quotes.models import BPOArticle

from .scatter import Scatter


class QueryStacks(Scatter):

    def __init__(self, corpus_dir: str, result_dir: str):

        """
        Set the input paths.
        """

        self.corpus_dir = corpus_dir

        self.result_dir = result_dir

        self.matches = []

    def args(self):

        """
        Generate corpus paths.
        """

        corpus = ChadhCorpus(self.corpus_dir)

        return corpus.slug_year_pairs()

    def process(self, slug: str, year: int):

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
