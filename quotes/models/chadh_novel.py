

from sqlalchemy import Column, Integer, String

from quotes.utils import scan_paths

from .base import Base


class ChadhNovel(Base):

    __tablename__ = 'chadh_novel'

    slug = Column(String, primary_key=True, autoincrement=False)

    year = Column(Integer)

    full_text = Column(String)
