

import os
import ujson
import uuid

from quotes.utils import scan_paths
from quotes.bpo import Article

from .scatter import Scatter


class ExtBPO(Scatter):

    def __init__(self, corpus_dir: str, result_dir: str):

        """
        Set the input paths.
        """

        self.corpus_dir = corpus_dir

        self.result_dir = result_dir

        self.articles = []

    def args(self):

        """
        Generate BPO paths.
        """

        yield from scan_paths(self.corpus_dir, '\.xml')

    def process(self, path: str):

        """
        Parse an article, flush the database row.
        """

        article = Article(path)

        self.articles.append(dict(
            record_id=article.record_id(),
            record_title=article.record_title(),
            publication_id=article.publication_id(),
            publication_title=article.publication_title(),
            publication_qualifier=article.publication_qualifier(),
            year=article.year(),
            source_type=article.source_type(),
            object_type=article.object_type(),
            contributor_role=article.contributor_role(),
            contributor_last_name=article.contributor_last_name(),
            contributor_first_name=article.contributor_first_name(),
            contributor_person_name=article.contributor_person_name(),
            contributor_original_form=article.contributor_original_form(),
            language_code=article.language_code(),
            text=article.text(),
        ))

        # Flush results when >1k.
        if len(self.articles) > 10000:
            self.flush()

    def flush(self):

        """
        Flush the matches to disk, clear cache.
        """

        path = os.path.join(
            self.result_dir,
            '{}.json'.format(str(uuid.uuid4())),
        )

        with open(path, 'w') as fh:
            ujson.dump(self.articles, fh)

        self.articles.clear()
