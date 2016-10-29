

import os
import uuid
import json


class RankCache:

    def __init__(self, path: str, size: int=1000):

        """
        Initialize the container.
        """

        self.path = os.path.abspath(path)

        self.size = size

        self._cache = []

    def add(self, result):

        """
        Add a result to the cache. If the new size is greater than the cache
        size, flush to disk.
        """

        self._cache.append(result)

        if len(self._cache) > self.size:
            self.flush()

    def flush(self) -> str:

        """
        Dump the cache to JSON, clear.
        """

        path = os.path.join(self.path, str(uuid.uuid4()))

        with open(path, 'w') as fh:
            json.dump(self._cache, fh)

        self._cache.clear()

        return path
