

import factory

from quotes.models import BPOArticle


class BPOArticleFactory(factory.Factory):

    class Meta:
        model = BPOArticle

    record_id = factory.Sequence(
        lambda n: n
    )

    year = 1900

    full_text = 'text'
