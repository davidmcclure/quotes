

import os


class C19Corpus:

    def __init__(self, path: str):

        """
        Canonicalize the path.
        """

        self.path = os.path.abspath(path)
