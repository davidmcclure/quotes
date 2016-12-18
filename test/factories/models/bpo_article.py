

import factory

from quotes.models import BPOArticle
from quotes.services import session


class BPOArticleFactory(factory.alchemy.SQLAlchemyModelFactory):

    class Meta:
        sqlalchemy_session = session
        model = BPOArticle

    record_id = factory.Sequence(
        lambda n: n
    )

    year = 1900

    text = 'text'
