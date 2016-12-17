

from quotes.models import ChadhNovel

from test.factories.models import ChadhNovelFactory


def test_alignment_pairs():

    n1 = ChadhNovelFactory(year=1910)
    n2 = ChadhNovelFactory(year=1920)
    n3 = ChadhNovelFactory(year=1930)

    pairs = list(ChadhNovel.alignment_pairs())

    for year in range(1910, 1921):
        assert dict(novel_id=n1.id, year=year) in pairs

    for year in range(1920, 1931):
        assert dict(novel_id=n2.id, year=year) in pairs

    for year in range(1930, 1941):
        assert dict(novel_id=n3.id, year=year) in pairs
