

from quotes.services import config
from quotes.jobs.query_stacks import QueryStacks


if __name__ == '__main__':

    job = QueryStacks(
        chadh_corpus_dir=config['chadh_corpus_dir'],
        chadh_slug='Chadwyck_British_1814_Scott_WaverleyorTis',
        stacks_db_url=config['stacks_db_url'],
        result_dir=config['result_dir'],
    )

    job()
