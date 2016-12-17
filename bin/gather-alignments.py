#!/usr/bin/env python


from quotes.services import config
from quotes.models import Alignment


if __name__ == '__main__':
    Alignment.gather(config['alignment_result_dir'])
