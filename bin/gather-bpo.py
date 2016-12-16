

from quotes.models import BPOArticle
from quotes.services import config


if __name__ == '__main__':
    BPOArticle.ingest(config['bpo_result_dir'])
