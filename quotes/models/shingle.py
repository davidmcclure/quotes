

from sqlalchemy import Column, Integer, String, PrimaryKeyConstraint

from quotes.singletons import config, session
from quotes.models import Base


class Shingle(Base):

    __tablename__ = 'shingle'

    __table_args__ = (
        PrimaryKeyConstraint(
            'key',
            'order',
            'char1',
            'char2',
        ),
    )

    key = Column(Integer, nullable=False)

    order = Column(Integer, nullable=False)

    char1 = Column(Integer, nullable=False)

    char2 = Column(Integer, nullable=False)
