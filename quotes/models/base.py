

from sqlalchemy import create_engine, event
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.engine.url import URL
from sqlalchemy.orm import sessionmaker, scoped_session

from quotes.singletons import session


class Base:

    @classmethod
    def connect(cls, url):

        """
        Set the database connection.
        """

        db_url = URL(**dict(
            drivername='sqlite',
            database=url,
        ))

        engine = create_engine(db_url)

        # Fix transaction bugs in pysqlite.
        # http://docs.sqlalchemy.org/en/rel_1_0/dialects/sqlite.html#pysqlite-serializable

        @event.listens_for(engine, 'connect')
        def connect(conn, record):
            conn.isolation_level = None

        @event.listens_for(engine, 'begin')
        def begin(conn):
            conn.execute('BEGIN')

        factory = sessionmaker(bind=engine)

        cls.session = scoped_session(factory)

        cls.query = cls.session.query_property()


Base = declarative_base(cls=Base)
