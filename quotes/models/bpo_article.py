

from sqlalchemy import Column, Integer, String

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

    full_text = Column(String)

    def ingest(cls, corpus_path: str):

        """
        Ingest BPO articles.
        """

        for path in scan_paths(corpus_path, '\.xml'):
            print(path)
