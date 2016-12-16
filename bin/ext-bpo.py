

from quotes.services import config
from quotes.jobs.ext_bpo import ExtBPO


if __name__ == '__main__':

    job = ExtBPO(
        corpus_dir=config['bpo_corpus_dir'],
        result_dir=config['bpo_result_dir'],
    )

    job()
