

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

    for novel, article in [
        (n1, a1),
        (n1, a2),
        (n2, a3),
        (n2, a4),
    ]:

        assert (
            Alignment.query
            .filter_by(a_id=novel.id, b_id=article.record_id)
            .one()
        )
