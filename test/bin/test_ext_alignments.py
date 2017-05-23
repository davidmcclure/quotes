

import pytest
import time

from subprocess import call

from quotes.models import Alignment
from quotes.services import session

from test.factories.models import QueryTextFactory, BPOArticleFactory


pytestmark = pytest.mark.usefixtures('mpi')


def test_ext_alignments():
    """ExtAlignments should record text -> Chadh alignments.
    """
    text = QueryTextFactory(text='aaa bbb ccc')

    a1 = BPOArticleFactory(text='aaa bbb ccc')
    a2 = BPOArticleFactory(text='aaa bbb ccc')

    session.commit()

    call(['mpirun', 'bin/ext-alignments.py', text.slug])
    call(['bin/gather-alignments.py'])

    # TODO: Test snippets?

    for a_id, b_id in [
        (text.id, a1.record_id),
        (text.id, a2.record_id),
    ]:

        assert (
            Alignment.query
            .filter_by(a_id=a_id, b_id=b_id)
            .one()
        )


# def test_multiple_matches():
    # """Record multiple matches for the same pair.
    # """
    # text = QueryTextFactory(text='aaa bbb ccc ddd eee fff')

    # a1 = BPOArticleFactory(text='aaa bbb ccc')
    # a2 = BPOArticleFactory(text='ddd eee fff')

    # session.commit()

    # call(['mpirun', 'bin/ext-alignments.py', text.slug])
    # call(['bin/gather-alignments.py'])

    # match1 = (
        # Alignment.query
        # .filter_by(a_id=text.id, b_id=a1.record_id)
        # .one()
    # )

    # match2 = (
        # Alignment.query
        # .filter_by(a_id=text.id, b_id=a2.record_id)
        # .one()
    # )

    # assert match1.a_start == 0
    # assert match1.b_start == 0
    # assert match1.size == 3

    # assert match2.a_start == 3
    # assert match2.b_start == 0
    # assert match2.size == 3


# def test_flush_matches():
    # """Matches should be flushed when the buffer goes over 1k.
    # """
    # text = QueryTextFactory(text='aaa bbb ccc')

    # for i in range(3000):
        # BPOArticleFactory(text='aaa bbb ccc')

    # session.commit()

    # call(['mpirun', 'bin/ext-alignments.py', text.slug])
    # call(['bin/gather-alignments.py'])

    # assert Alignment.query.count() == 3000
