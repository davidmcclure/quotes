

import re
import json
import os
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

    @classmethod
    def from_chadh_c19(cls, path: str):

        """
        Read from a Chadwyck Healey C19 file.
        """

        slug = os.path.splitext(os.path.basename(path))[0]

        year = int(re.search('[0-9]{4}', slug).group(0))

        with open(path) as fh:
            return cls(fh.read(), dict(slug=slug, year=year))

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
        t2 = max(start-padding, 0)
        char1 = self.tokens[t2].char1

        # snippet start
        char2 = self.tokens[start].char1

        # snippet end
        char3 = self.tokens[start+size-1].char2

        # padding end
        t2 = min(start+size-1+padding, len(self.tokens)-1)
        char4 = self.tokens[t2].char2

        return map(clean_text, [
            self.text[char1:char2],
            self.text[char2:char3],
            self.text[char3:char4],
        ])
