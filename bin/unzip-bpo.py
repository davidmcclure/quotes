

from quotes.services import config
from quotes.jobs.unzip_bpo import UnzipBPO


if __name__ == '__main__':
    job = UnzipBPO(corpus_dir=config['bpo_corpus_dir'])
    job()
