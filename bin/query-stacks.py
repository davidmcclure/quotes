

from quotes.jobs.query_stacks import QueryStacks


if __name__ == '__main__':

    # TODO: Parametrize.
    query = QueryStacks(
        '/scratch/PI/malgeehe/data/stacks/ext/chicago',
        '/scratch/PI/malgeehe/data/quotes/pg10.txt',
    )

    query()
