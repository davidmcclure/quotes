

import pytest

from quotes.services import session
from quotes.jobs.ext_alignments import Tasks

from test.factories.models import ChadhNovelFactory, BPOArticleFactory


pytestmark = pytest.mark.usefixtures('db')


def test_from_chadh():
    """Tasks.from_chadh() should provide all tasks from the Chadwyck novels.
    """
    n1 = ChadhNovelFactory(year=1910)
    n2 = ChadhNovelFactory(year=1920)
    n3 = ChadhNovelFactory(year=1930)

    for year in range(1910, 1941):
        BPOArticleFactory(year=year)

    session.commit()

    tasks = Tasks.from_chadh()

    partitions = tasks.partitions(3)

    args = partitions.make_args()

    # flatten list
    # check for each novel + year
