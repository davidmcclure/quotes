

from invoke import task

from quotes.singletons import config
from quotes.models import Base


@task
def init_db(ctx):

    """
    Create database tables.
    """

    engine = config.build_sqla_engine()

    Base.metadata.create_all(engine)
