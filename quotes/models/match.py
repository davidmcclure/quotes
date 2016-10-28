

from sqlalchemy import Column, Integer, String, PrimaryKeyConstraint

from .base import Base


class Match(Base):

    __tablename__ = 'match'

    __table_args__ = (
        PrimaryKeyConstraint(
            'a_slug',
            'b_corpus',
            'b_identifier',
        ),
    )

    a_slug = Column(String, nullable=False)

    b_corpus = Column(String, nullable=False)

    b_identifier = Column(String, nullable=False)

    a_start = Column(Integer, nullable=False)

    b_start = Column(Integer, nullable=False)

    size = Column(Integer, nullable=False)

    a_prefix = Column(String, nullable=False)

    a_snippet = Column(String, nullable=False)

    a_suffix = Column(String, nullable=False)

    b_prefix = Column(String, nullable=False)

    b_snippet = Column(String, nullable=False)

    b_suffix = Column(String, nullable=False)
