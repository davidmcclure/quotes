

import re
import json
import bz2

from wordfreq import top_n_list
from difflib import SequenceMatcher
from collections import namedtuple

from quotes.utils import clean_text


Token = namedtuple('Tuple', [
    'token',
    'char1',
    'char2',
])


blacklist = set(top_n_list('en', 200))


class Text:

    @classmethod
    def from_stacks(cls, path: str):

        """
        Read from a Stacks JSON file.
        """

        with bz2.open(path, 'rt') as fh:

            metadata = json.loads(fh.read())

            text = metadata.pop('plain_text')

            return cls(text, metadata)

    def __init__(self, text: str, metadata: dict=None):

        """
        Tokenize the text.
        """

        self.text = text

        self.metadata = metadata or {}

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

    def match(self, text, min_size: int=3):

        """
        Find alignments with another text.
        """

        s_tokens = self.sequence()
        q_tokens = text.sequence()

        matcher = SequenceMatcher(a=s_tokens, b=q_tokens)

        for match in matcher.get_matching_blocks():
            if match.size >= min_size:
                yield match

    def snippet(self, start: int, size: int, padding: int=10):

        """
        Hydrate a snippet.
        """

        # padding start
        char1 = self.tokens[start-padding].char1

        # snippet start
        char2 = self.tokens[start].char1

        # snippet end
        char3 = self.tokens[start+size-1].char2

        # padding end
        end = min(start+size-1+padding, len(self.tokens)-1)
        char4 = self.tokens[end].char2

        return map(clean_text, [
            self.text[char1:char2],
            self.text[char2:char3],
            self.text[char3:char4],
        ])
