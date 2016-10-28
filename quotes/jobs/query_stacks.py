

from quotes.text import Text
from quotes.utils import scan_paths

from .scatter import Scatter


class QueryStacks(Scatter):

    def __init__(self, corpus_path: str, query_path: str):

        """
        Set the input paths.
        """

        self.corpus_path = corpus_path

        self.text = Text.from_txt(query_path)

    def args(self):

        """
        Generate corpus paths.
        """

        yield from scan_paths(self.corpus_path, '\.bz2')

    def process(self, path: str):

        """
        Hydrate a text from the corpus, align with the query.
        """

        pass
