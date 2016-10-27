

import re

from boltons.iterutils import windowed_iter
from spooky import hash32


class Text:

    @classmethod
    def from_file(cls, path: str):

        """
        Read from a text file.
        """

        with open(path) as fh:
            return cls(fh.read())

    def __init__(self, text: str):

        """
        Tokenize the text.
        """

        self.text = text

        self.tokens = re.findall('[a-z]+', self.text.lower())

    def hashed_shingles(self, n: int):

        """
        Generate "shingles," with the tokens hashed to an integer.
        """

        for i, ngram in enumerate(windowed_iter(self.tokens, n)):
            yield (hash32('.'.join(ngram)), i)
