

import pytest

from subprocess import call

from quotes.models import Alignment
from quotes.services import session

from test.factories.models import ChadhNovelFactory, BPOArticleFactory


pytestmark = pytest.mark.usefixtures('mpi')


def test_ext_alignments():

    """
    ExtAlignments should record BPO -> Chadh alignments.
    """

    n1 = ChadhNovelFactory(text='aaa bbb ccc')
    n2 = ChadhNovelFactory(text='ddd eee fff')

    a1 = BPOArticleFactory(text='aaa bbb ccc')
    a2 = BPOArticleFactory(text='aaa bbb ccc')

    a3 = BPOArticleFactory(text='ddd eee fff')
    a4 = BPOArticleFactory(text='ddd eee fff')

    session.commit()

    call(['mpirun', 'bin/ext-alignments.py'])
    call(['bin/gather-alignments.py'])

    # TODO: Test snippets?

    for a_id, b_id in [
        (n1.id, a1.record_id),
        (n1.id, a2.record_id),
        (n2.id, a3.record_id),
        (n2.id, a4.record_id),
    ]:

        assert (
            Alignment.query
            .filter_by(a_id=a_id, b_id=b_id)
            .one()
        )


def test_year_range():

    """
    Just check the 10 years after publication.
    """

    n1 = ChadhNovelFactory(text='aaa bbb ccc', year=1900)

    a1 = BPOArticleFactory(text='aaa bbb ccc', year=1905)
    a2 = BPOArticleFactory(text='aaa bbb ccc', year=1915)

    session.commit()

    call(['mpirun', 'bin/ext-alignments.py'])
    call(['bin/gather-alignments.py'])

    assert (
        Alignment.query
        .filter_by(a_id=n1.id, b_id=a1.record_id)
        .one()
    )

    # Ignore the article >10 years after publication.

    assert not (
        Alignment.query
        .filter_by(a_id=n1.id, b_id=a2.record_id)
        .first()
    )


def test_multiple_matches():

    """
    Record multiple matches for the same pair.
    """

    n1 = ChadhNovelFactory(text='aaa bbb ccc ddd eee fff')

    a1 = BPOArticleFactory(text='aaa bbb ccc')
    a2 = BPOArticleFactory(text='ddd eee fff')

    session.commit()

    call(['mpirun', 'bin/ext-alignments.py'])
    call(['bin/gather-alignments.py'])

    match1 = (
        Alignment.query
        .filter_by(a_id=n1.id, b_id=a1.record_id)
        .one()
    )

    match2 = (
        Alignment.query
        .filter_by(a_id=n1.id, b_id=a2.record_id)
        .one()
    )

    assert match1.a_start == 0
    assert match1.b_start == 0
    assert match1.size == 3

    assert match2.a_start == 3
    assert match2.b_start == 0
    assert match2.size == 3
