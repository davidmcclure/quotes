

import os
import pickle
import uuid
import dataset

from quotes.text import Text

from .scatter import Scatter


class QueryStacks(Scatter):

    def __init__(self,
                 chadh_corpus_dir: str,
                 chadh_slug: str,
                 stacks_db_url: str,
                 result_dir: str):

        """
        Set the input paths.
        """

        fname = '{}.txt'.format(chadh_slug)

        path = os.path.join(chadh_corpus_dir, fname)

        self.text = Text.from_chadh_c19(path)

        self.stacks_db = dataset.connect(stacks_db_url)

        self.result_dir = result_dir

        self.matches = []

    def args(self):

        """
        Generate corpus paths.
        """

        pub_year = self.text.metadata['year']

        query = '''
        SELECT path FROM text
        WHERE corpus = "bpo" and year >= {} and year <= {}
        '''.format(pub_year, pub_year+10)

        return [r['path'] for r in self.stacks_db.query(query)]

    def process(self, path: str):

        """
        Hydrate a text from the corpus, align with the query.
        """

        stacks_text = Text.from_stacks(path)

        matches = self.text.match(stacks_text)

        for m in matches:

            a_prefix, a_snippet, a_suffix = self.text.snippet(m.a, m.size)
            b_prefix, b_snippet, b_suffix = stacks_text.snippet(m.b, m.size)

            self.matches.append(dict(

                a_slug=self.text.metadata['slug'],

                b_corpus=stacks_text.metadata['corpus'],
                b_identifier=stacks_text.metadata['identifier'],
                b_title=stacks_text.metadata['title'],
                b_author=stacks_text.metadata['author_full'],

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

    def flush(self):

        """
        Flush matches to disk.
        """

        # TODO: Use ujson.

        path = os.path.join(self.result_dir, str(uuid.uuid4()))

        with open(path, 'wb') as fh:
            pickle.dump(self.matches, fh)
