import logging

from vcs_mirrors.lib.utils import sync_one


def configure_argparse(subparser):
    pass

def execute(config, args):
    result = 0
    for repo in config['repos'].keys():
        logging.info('Syncing "%s"' % repo)
        if sync_one(repo, config) == False:
            result = 1

    return result
