

from quotes.services import config
from quotes.models import Match


if __name__ == '__main__':
    Match.gather(config['match_result_dir'])