

import ujson

from datetime import datetime as dt
from sqlalchemy import Column, Integer, String

from quotes.services import session
from quotes.utils import scan_paths

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

    text = Column(String)

    @classmethod
    def ingest(cls, result_dir: str):

        """
        Ingest BPO articles.
        """

        paths = scan_paths(result_dir, '\.json')

        # Walk paths.
        for i, path in enumerate(paths):
            with open(path) as fh:

                # Bulk-insert articles.
                session.bulk_insert_mappings(cls, ujson.load(fh))
                session.commit()

                print(dt.now().isoformat(), i)

    @classmethod
    def ids_in_years(cls, year1: int, year2: int):

        """
        Get ids for all articles in a range of years.
        """

        query = (
            session
            .query(cls.record_id)
            .filter(cls.year >= year1, cls.year <= year2)
        )

        return [r[0] for r in query]
