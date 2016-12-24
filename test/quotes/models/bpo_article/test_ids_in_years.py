

from quotes.models import BPOArticle

from test.factories.models import BPOArticleFactory


def test_ids_in_years():

    a1 = BPOArticleFactory(year=1900)
    a2 = BPOArticleFactory(year=1905)
    a3 = BPOArticleFactory(year=1910)
    a4 = BPOArticleFactory(year=1911)

    ids = BPOArticle.ids_in_years(1900, 1910)

    assert a1.record_id in ids
    assert a2.record_id in ids
    assert a3.record_id in ids

    assert a4.record_id not in ids
