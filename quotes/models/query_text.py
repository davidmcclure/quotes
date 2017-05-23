

import os

from sqlalchemy import Column, Integer, String

from quotes.services import session

from .base import Base


class QueryText(Base):

    __tablename__ = 'query_text'

    id = Column(Integer, primary_key=True)

    slug = Column(String, unique=True, nullable=False)

    text = Column(String, nullable=False)

    @classmethod
    def ingest(cls, slug, path):
        """Load a text from a file path.

        Args:
            slug (str)
            path (str)
        """
        with open(path) as fh:
            session.add(cls(slug=slug, text=fh.read()))
            session.commit()
