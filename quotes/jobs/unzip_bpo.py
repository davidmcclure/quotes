

import os
import zipfile

from quotes.utils import scan_paths

from .scatter import Scatter


class UnzipBPO(Scatter):

    def __init__(self, corpus_dir: str):

        """
        Set the input paths.
        """

        self.corpus_dir = corpus_dir

    def args(self):

        """
        Generate BPO archive paths.
        """

        yield from scan_paths(self.corpus_dir, '\.zip')

    def process(self, path: str):

        """
        Unzip the archive into a new directory.
        """

        xml_dir = os.path.splitext(os.path.basename(path))[0]

        with zipfile.ZipFile(path) as fh:
            fh.extractall(xml_dir)
