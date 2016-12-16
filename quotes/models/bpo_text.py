

from sqlalchemy import Column, Integer, String
from .base import Base


class BPOText(Base):

    __tablename__ = 'bpo_text'

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
