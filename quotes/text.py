

import re

from collections import namedtuple
from wordfreq import top_n_list


Token = namedtuple('Tuple', [
    'token',
    'char1',
    'char2',
])


blacklist = set(top_n_list('en', 500))


class Text:

    @classmethod
    def from_txt(cls, path: str):

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
            if m.group(0) not in blacklist

        ]

    def sequence(self):

        """
        Provide the raw token stream.
        """

        return [t.token for t in self.tokens]
