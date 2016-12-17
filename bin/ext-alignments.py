

from quotes.services import config
from quotes.jobs.ext_alignments import ExtAlignments


if __name__ == '__main__':
    job = ExtAlignments(result_dir=config['alignment_result_dir'])
    job()
