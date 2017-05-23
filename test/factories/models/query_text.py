

import factory

from quotes.models import QueryText
from quotes.services import session


class QueryTextFactory(factory.alchemy.SQLAlchemyModelFactory):

    class Meta:
        sqlalchemy_session = session
        model = QueryText

    slug = factory.Sequence(
        lambda n: 'text-{}'.format(n),
    )

    text = 'text'
