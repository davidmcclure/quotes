

from quotes.text import Text
from quotes.utils import scan_paths
from quotes.models import Match

from .scatter import Scatter


class QueryStacks(Scatter):

    def __init__(self, corpus_path: str, text_path: str):

        """
        Set the input paths.
        """

        self.corpus_path = corpus_path

        self.text = Text.from_txt(text_path)

    def args(self):

        """
        Generate corpus paths.
        """

        yield from scan_paths(self.corpus_path, '\.bz2')

    def process(self, path: str):

        """
        Hydrate a text from the corpus, align with the query.
        """

        text = Text.from_stacks(path)

        matches = self.text.match(text)

        # TODO|dev
        for m in matches:
            print('QUERY', self.text.bold_snippet(m.a, m.size))
            print('MATCH', text.bold_snippet(m.b, m.size))
            print('-'*50)

    def flush(self):
        pass
