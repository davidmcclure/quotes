

import os
import ujson
import uuid

from quotes.text import Text
from quotes.models import ChadhNovel, BPOArticle

from .scatter import Scatter


class ExtAlignments(Scatter):

    def __init__(self, result_dir: str):

        """
        Set the input paths.
        """

        self.result_dir = result_dir

        self.matches = []

    def args(self):

        """
        Generate (novel id, year) pairs.
        """

        return ChadhNovel.alignment_pairs()

    def process(self, novel_id: str, year: int):

        """
        Query BPO texts in a given year against a novel.
        """

        # Hydrate the Chadwyck novel.
        novel = ChadhNovel.query.get(novel_id)
        a = Text(novel.text)

        # Query BPO articles in the year.
        articles = BPOArticle.query.filter_by(year=year)

        for article in articles:

            b = Text(article.text)

            # Align article -> novel.
            matches = a.match(b)

            # Record matches.
            for m in matches:

                a_prefix, a_snippet, a_suffix = a.snippet(m.a, m.size)
                b_prefix, b_snippet, b_suffix = b.snippet(m.b, m.size)

                self.matches.append(dict(

                    a_id=novel.id,
                    b_id=article.record_id,

                    a_start=m.a,
                    b_start=m.b,
                    size=m.size,

                    a_prefix=a_prefix,
                    a_snippet=a_snippet,
                    a_suffix=a_suffix,

                    b_prefix=b_prefix,
                    b_snippet=b_snippet,
                    b_suffix=b_suffix,

                ))

        # Flush results when >1k.
        if len(self.matches) > 1000:
            self.flush()

    def flush(self):

        """
        Flush the matches to disk, clear cache.
        """

        path = os.path.join(self.result_dir, str(uuid.uuid4()))

        with open(path, 'w') as fh:
            ujson.dump(self.matches, fh)

        self.matches.clear()
