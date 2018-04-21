import logging

from vcs_mirrors.lib.utils import sync_one


def configure_argparse(subparser):
    subparser.add_argument('name',
                           help='Internal repository name')


def execute(config, args):
    logging.info('Syncing "%s"' % args['name'])
    if sync_one(args['name'], config) == False:
        return 1

    return 0
