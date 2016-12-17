

from sqlalchemy import Column, Integer, String

from quotes.utils import scan_paths

from .base import Base


class ChadhNovel(Base):

    __tablename__ = 'chadh_novel'

    id = Column(Integer, primary_key=True)

    slug = Column(String, unique=True, nullable=False)

    year = Column(Integer, nullable=False)

    full_text = Column(String, nullable=False)
