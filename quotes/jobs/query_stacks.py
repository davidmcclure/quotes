

import os
import pickle
import uuid

from quotes.utils import scan_paths
from quotes.text import RawText, StacksText
from quotes.models import Match

from .scatter import Scatter


class QueryStacks(Scatter):

    def __init__(self, corpus_dirs, result_dir: str,
            text_slug: str, text_path: str):

        """
        Set the input paths.
        """

        self.corpus_dirs = corpus_dirs

        self.result_dir = result_dir

        self.text_slug = text_slug

        self.text = RawText.from_file(text_path)

        self.matches = []

    def args(self):

        """
        Generate corpus paths.
        """

        for cdir in self.corpus_dirs:
            yield from scan_paths(cdir, '\.bz2')

    def process(self, path: str):

        """
        Hydrate a text from the corpus, align with the query.
        """

        text = StacksText.from_file(path)

        if text.year < 1814 and text.year > 1824:
            return

        matches = self.text.match(text)

        for m in matches:

            a_prefix, a_snippet, a_suffix = self.text.snippet(m.a, m.size)
            b_prefix, b_snippet, b_suffix = text.snippet(m.b, m.size)

            self.matches.append(dict(

                a_slug=self.text_slug,

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

        path = os.path.join(self.result_dir, str(uuid.uuid4()))

        with open(path, 'wb') as fh:
            pickle.dump(self.matches, fh)
