

from quotes.singletons import config
from quotes.jobs.query_stacks import QueryStacks


if __name__ == '__main__':

    job = QueryStacks(
        corpus_dirs=config['stacks_dirs'],
        result_dir=config['result_dir'],
        text_path=config['text_paths']['hamlet'],
        text_slug='kjb',
    )

    job()
