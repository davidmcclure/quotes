

import factory

from quotes.models import ChadhNovel


class ChadhNovelFactory(factory.Factory):

    class Meta:
        model = ChadhNovel

    slug = factory.Sequence(
        lambda n: 'novel-{}'.format(n),
    )

    year = 1900

    text = 'text'
