

import factory

from quotes.models import ChadhNovel
from quotes.services import session


class ChadhNovelFactory(factory.alchemy.SQLAlchemyModelFactory):

    class Meta:
        sqlalchemy_session = session
        model = ChadhNovel

    slug = factory.Sequence(
        lambda n: 'novel-{}'.format(n),
    )

    year = 1900

    text = 'text'
