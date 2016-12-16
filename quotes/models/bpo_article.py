

import ujson

from sqlalchemy import Column, Integer, String

from quotes.services import session
from quotes.utils import scan_paths, grouper

from .base import Base


class BPOArticle(Base):

    __tablename__ = 'bpo_article'

    record_id = Column(Integer, primary_key=True, autoincrement=False)

    record_title = Column(String)

    publication_id = Column(Integer)

    publication_title = Column(String)

    publication_qualifier = Column(String)

    year = Column(Integer)

    source_type = Column(String)

    object_type = Column(String)

    contributor_role = Column(String)

    contributor_last_name = Column(String)

    contributor_first_name = Column(String)

    contributor_person_name = Column(String)

    contributor_original_form = Column(String)

    language_code = Column(String)

    full_text = Column(String)

    @classmethod
    def ingest(cls, result_dir: str, n: int=1000):

        """
        Ingest BPO articles.
        """

        paths = scan_paths(result_dir, '\.json')

        groups = grouper(paths, n)

        for i, group in enumerate(groups):

            mappings = [ujson.load(open(path)) for path in group]

            session.bulk_insert_mappings(cls, mappings)
            print((i+1)*n)

        session.commit()
