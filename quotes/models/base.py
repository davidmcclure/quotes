

from sqlalchemy import create_engine, event
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.engine.url import URL
from sqlalchemy.orm import sessionmaker, scoped_session


class Base:

    @classmethod
    def connect(cls, url=None):

        """
        Set the database connection.
        """

        db_url = URL(**dict(
            drivername='sqlite',
            database=url,
        ))

        engine = create_engine(db_url)

        # Fix transaction bugs in pysqlite.

        @event.listens_for(engine, 'connect')
        def connect(conn, record):
            conn.isolation_level = None

        @event.listens_for(engine, 'begin')
        def begin(conn):
            conn.execute('BEGIN')

        factory = sessionmaker(bind=engine)

        session = scoped_session(factory)

        # Attach query shortcut.
        cls.query = session.query_property()

        # Create tables.
        cls.metadata.create_all(engine)

        return session

    def columns(self):

        """
        Get a list of column names.

        Returns: list
        """

        return [c.name for c in self.__table__.columns]

    def __iter__(self):

        """
        Generate column / value tuples.

        Yields: (key, val)
        """

        for key in self.columns():
            yield (key, getattr(self, key))


Base = declarative_base(cls=Base)
