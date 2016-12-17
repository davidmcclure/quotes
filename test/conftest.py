

import pytest

from quotes.services import config as _config, session
from quotes.models import Base


@pytest.fixture(scope='session', autouse=True)
def init_testing_db():

    """
    Drop and recreate the tables.
    """

    engine = _config.build_sqla_engine()

    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)


@pytest.yield_fixture
def db():

    """
    Reset the testing database.
    """

    session.begin_nested()

    yield

    session.remove()


@pytest.yield_fixture
def config():

    """
    Clear changes to the config dict.
    """

    # Copy settings.
    old = _config.copy()

    yield _config

    # Restore settings.
    _config.clear()
    _config.update(old)


@pytest.yield_fixture
def mpi(config):

    """
    Write the patched config to /tmp/.lint.yml.
    """

    config.write_tmp()

    yield

    config.clear_tmp()

    session.remove()

    init_testing_db()
