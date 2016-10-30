

import pickle

from quotes.utils import scan_paths
from quotes.text import RawText, StacksText
from quotes.models import Match

from .scatter import Scatter


class QueryStacks(Scatter):

    def __init__(self, corpus_path: str, slug: str, text_path: str):

        """
        Set the input paths.
        """

        self.corpus_path = corpus_path

        self.slug = slug

        self.text = RawText.from_file(text_path)

        self.matches = []

    def args(self):

        """
        Generate corpus paths.
        """

        yield from scan_paths(self.corpus_path, '\.bz2')

    def process(self, path: str):

        """
        Hydrate a text from the corpus, align with the query.
        """

        text = StacksText.from_file(path)

        matches = self.text.match(text)

        for m in matches:

            a_prefix, a_snippet, a_suffix = self.text.snippet(m.a, m.size)
            b_prefix, b_snippet, b_suffix = text.snippet(m.b, m.size)

            self.matches.append(dict(

                a_slug=self.slug,

                b_corpus=text.metadata['corpus'],
                b_identifier=text.metadata['identifier'],
                b_title=text.metadata['title'],
                b_author=text.metadata['author_full'],

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

    def flush(self):

        """
        Flush matches to disk.
        """

        with open('test', 'wb') as fh:
            pickle.dump(self.matches, fh)
