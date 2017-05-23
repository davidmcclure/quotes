

import ujson

from datetime import datetime as dt

from sqlalchemy import (
    Column,
    Integer,
    String,
    PrimaryKeyConstraint,
    ForeignKey,
)

from sqlalchemy.orm import relationship

from quotes.services import session
from quotes.utils import scan_paths

from .base import Base


class Alignment(Base):

    __tablename__ = 'alignment'

    __table_args__ = (
        PrimaryKeyConstraint(
            'a_id',
            'b_id',
            'a_start',
            'b_start',
        ),
    )

    # Texts
    a_id = Column(Integer, ForeignKey('query_text.id'))
    b_id = Column(Integer, ForeignKey('bpo_article.record_id'))

    query_text = relationship('QueryText')
    bpo_article = relationship('BPOArticle')

    # Match
    a_start = Column(Integer, nullable=False)
    b_start = Column(Integer, nullable=False)
    size = Column(Integer, nullable=False)

    # A snippet
    a_prefix = Column(String, nullable=False)
    a_snippet = Column(String, nullable=False)
    a_suffix = Column(String, nullable=False)

    # B snippet
    b_prefix = Column(String, nullable=False)
    b_snippet = Column(String, nullable=False)
    b_suffix = Column(String, nullable=False)

    @classmethod
    def gather(cls, result_dir: str):

        """
        Bulk-insert alignments.
        """

        paths = scan_paths(result_dir, '\.json')

        # Walk paths.
        for i, path in enumerate(paths):
            with open(path, 'rb') as fh:

                mappings = ujson.load(fh)

                # Bulk-insert matches.
                session.bulk_insert_mappings(cls, mappings)
                session.commit()

                print(dt.now().isoformat(), i)
