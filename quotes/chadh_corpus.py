

import os
import re

from quotes.utils import scan_paths


class ChadhCorpus:

    def __init__(self, path: str):

        """
        Canonicalize the corpus path.
        """

        self.path = os.path.abspath(path)

    def slugs(self):

        """
        Generate a list of slugs from the corpus.
        """

        for path in scan_paths(self.path, '\.txt'):
            yield os.path.splitext(os.path.basename(path))[0]

    def slug_year_pairs(self, n=10):

        """
        Generate a list of (slug, year) pairs for the N years after the
        publication of each book.
        """

        for slug in self.slugs():

            pub_year = int(re.search('[0-9]{4}', slug).group())

            for year in range(pub_year, pub_year+n+1):
                yield dict(slug=slug, year=year)
