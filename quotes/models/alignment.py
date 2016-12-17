

import pickle

from sqlalchemy import (
    Column,
    Integer,
    String,
    PrimaryKeyConstraint,
    ForeignKey,
)

from scandir import scandir

from quotes.services import session

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
    a_id = Column(Integer, ForeignKey('chadh_novel.id'))
    b_id = Column(Integer, ForeignKey('bpo_article.record_id'))

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

        # Gather pickle paths.
        paths = [
            d.path
            for d in scandir(result_dir)
            if d.is_file()
        ]

        # Walk paths.
        for i, path in enumerate(paths):
            with open(path, 'rb') as fh:

                mappings = pickle.load(fh)

                # Bulk-insert the rows.
                session.bulk_insert_mappings(cls, mappings)
                print(i)

        session.commit()
