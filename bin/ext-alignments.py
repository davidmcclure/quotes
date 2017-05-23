#!/usr/bin/env python


import click

from quotes.services import config, session
from quotes.jobs.ext_alignments import ExtAlignments


@click.command()
@click.argument('slug')
def main(slug):
    job = ExtAlignments(slug, result_dir=config['alignment_result_dir'])
    job()


if __name__ == '__main__':
    main()
