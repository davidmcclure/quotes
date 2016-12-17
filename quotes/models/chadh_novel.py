

import os
import re

from sqlalchemy import Column, Integer, String

from quotes.utils import scan_paths
from quotes.services import session

from .base import Base


class ChadhNovel(Base):

    __tablename__ = 'chadh_novel'

    id = Column(Integer, primary_key=True)

    slug = Column(String, unique=True, nullable=False)

    year = Column(Integer, nullable=False)

    text = Column(String, nullable=False)

    @classmethod
    def ingest(cls, corpus_dir: str):

        """
        Ingest texts.
        """

        for path in scan_paths(corpus_dir, '\.txt'):

            slug = os.path.splitext(os.path.basename(path))[0]

            year = int(re.search('[0-9]{4}', slug).group())

            with open(path) as fh:
                novel = cls(slug=slug, year=year, text=fh.read())
                session.add(novel)

        session.commit()

    @classmethod
    def alignment_pairs(cls, years=10):

        """
        For each novel, generate (novel id, year) pairs for the N years after
        the publication of each novel.
        """

        for novel in cls.query.all():
            for year in range(novel.year, novel.year+years+1):
                yield (novel.id, year)
