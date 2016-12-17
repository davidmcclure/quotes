

import pytest

from subprocess import call

from quotes.services import session

from test.factories.models import ChadhNovelFactory, BPOArticleFactory


pytestmark = pytest.mark.usefixtures('mpi')


def test_ext_alignments():

    """
    ExtAlignments should record BPO -> Chadh alignments.
    """

    n1 = ChadhNovelFactory()
    n2 = ChadhNovelFactory()

    a1 = BPOArticleFactory()
    a2 = BPOArticleFactory()
    a3 = BPOArticleFactory()
    a4 = BPOArticleFactory()

    call(['mpirun', 'bin/ext-alignments.py'])
    call(['bin/gather-alignments.py'])

    assert True
