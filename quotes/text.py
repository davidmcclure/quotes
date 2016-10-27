

import re

from collections import namedtuple

from boltons.iterutils import windowed_iter
from spooky import hash64


Token = namedtuple('Tuple', ['token', 'char1', 'char2'])


Shingle = namedtuple('Shingle', ['key', 'order', 'char1', 'char2'])


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

        self.tokens = [

            Token(
                token=m.group(0),
                char1=m.start(),
                char2=m.end(),
            )

            for m in re.finditer('[a-z]+', self.text.lower())

        ]

    def shingles(self, n: int):

        """
        Generate "shingles," with the tokens hashed to an integer.
        """

        for i, ngram in enumerate(windowed_iter(self.tokens, n)):

            tokens = [n.token for n in ngram]

            key = hash64('.'.join(tokens))

            char1 = ngram[0].char1
            char2 = ngram[-1].char2

            yield Shingle(
                key=key,
                order=i,
                char1=char1,
                char2=char2,
            )
