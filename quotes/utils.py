

import re
import scandir
import os
import psutil

from contextlib import contextmanager
from itertools import islice, chain


def clean_text(text: str) -> str:
    """Clean a raw text string.
    """
    return re.sub('\s{2,}|\n', ' ', text.strip())


def scan_paths(root_dir: str, pattern: str):
    """Walk a directory and yield file paths that match a pattern.
    """
    root_dir = os.path.abspath(root_dir)

    pattern = re.compile(pattern)

    for root, dirs, files in scandir.walk(root_dir, followlinks=True):
        for name in files:

            # Match the extension.
            if pattern.search(name):
                yield os.path.join(root, name)


def mem_pct():
    """Get the percentage of available memory used by the process.

    Returns: float
    """
    mem = psutil.virtual_memory()

    return mem.percent


def grouper(iterable, size):
    """Yield "groups" from an iterable.

    Args:
        iterable (iter): The iterable.
        size (int): The number of elements in each group.

    Yields:
        The next group.
    """
    source = iter(iterable)

    while True:
        group = islice(source, size)
        yield chain([next(group)], group)


@contextmanager
def open_makedirs(fpath, *args, **kwargs):
    """Create the directory for a file, open it.
    """
    path = os.path.dirname(fpath)

    os.makedirs(path, exist_ok=True)

    with open(fpath, *args, **kwargs) as fh:
        yield fh
