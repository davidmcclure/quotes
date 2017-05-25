#!/usr/bin/env python


import os
import ujson
import uuid
import click

from datetime import datetime as dt
from functools import partial
from multiprocessing import Pool, Manager

from quotes.models import BPOArticle, QueryText
from quotes.text import Text
from quotes.services import config, session
from quotes.utils import mem_pct


def align_year(lock, text, year):
    """Given a year, align the text identifier by slug with all BPO articles in
    the passed year.

    Args:
        slug (str)
        year (int)
    """
    # Wrap the query text.
    a = Text(text.text)

    # Load articles in year.
    lock.acquire()
    articles = session().query(BPOArticle).filter_by(year=year)
    lock.release()

    matches = []
    for i, article in enumerate(articles):

        try:

            b = Text(article.text)

            # Record matches.
            for m in a.match(b):

                a_prefix, a_snippet, a_suffix = a.snippet(m.a, m.size)
                b_prefix, b_snippet, b_suffix = b.snippet(m.b, m.size)

                matches.append(dict(

                    a_id=text.id,
                    b_id=article.record_id,

                    a_start=m.a,
                    b_start=m.b,
                    size=m.size,

                    a_prefix=a_prefix,
                    a_snippet=a_snippet,
                    a_suffix=a_suffix,

                    b_prefix=b_prefix,
                    b_snippet=b_snippet,
                    b_suffix=b_suffix,

                ))

        except Exception as e:
            print(e)

        if i % 1000 == 0:
            print('align', year, i, mem_pct(), dt.now().isoformat())

    return matches


@click.command()
@click.argument('slug')
def main(slug):
    """Align a text against all of BPO.

    Args:
        slug (str)
        result_dir (str)
    """
    # Hydrate the query text.
    text = QueryText.query.filter_by(slug=slug).one()

    # Get list of years.
    years = BPOArticle.years()

    session.close()

    # Get the lock instance.
    manager = Manager()
    lock = manager.Lock()

    # Bind lock + text to worker.
    worker = partial(align_year, lock, text)

    with Pool() as pool:

        results = pool.imap_unordered(worker, years)

        for matches in results:

            fname = str(uuid.uuid4())

            path = os.path.join(
                config['alignment_result_dir'],
                '{}.json'.format(fname),
            )

            with open(path, 'w') as fh:
                ujson.dump(matches, fh)


if __name__ == '__main__':
    main()
