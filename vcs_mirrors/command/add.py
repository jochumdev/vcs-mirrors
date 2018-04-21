import logging

from zope.interface.verify import verifyObject
from zope.interface.exceptions import BrokenImplementation

from vcs_mirrors.lib.interfaces import IHost
from vcs_mirrors.lib.loader import load_hosts
from vcs_mirrors.lib.utils import get_url_host


def configure_argparse(subparser):
    subparser.add_argument('-f', '--force',
                           help='force fetch and push (default False)',
                           dest='force',
                           action='store_true',
                           default=False,
                           required=False)

    subparser.add_argument('-p', '--prune',
                           help='Prune on fetch and push (default False)',
                           dest='prune',
                           action='store_true',
                           default=False,
                           required=False)

    subparser.add_argument('name',
                           help='Internal repository name, for example pcdummy/vcs-mirrors')

    subparser.add_argument('source',
                           help='The source VCS repo URL')

    subparser.add_argument('dest',
                           help='The destination VCS repo URL or <HOST>:<REPO>, if <REPO> is not given we use "name" as REPO')


def execute(config, args):
    if args['name'] in config['repos']:
        logging.fatal('The repository "%s" has already been registered.' % args['name'])
        return 1

    if get_url_host(args['source']) is None:
        logging.fatal('No repository handler for source URL "%s" found.' % args['source'])
        return 1

    dest = args['dest']
    dest_host = None
    dest_split = args['dest'].split(':')
    if dest_split[0] in config['hosts']:
        cfg_host = config['hosts'][dest_split[0]]

        cfg_type = cfg_host['type'].lower()

        hosts = load_hosts()
        for cls in hosts.values():
            if cls.TYPE != cfg_type:
                continue

            dest_host = cls(dest_split[0], cfg_host)
            break

        if dest_host is None:
            logging.fatal('Host type "%s" not implemented.' % cfg_type)
            return 1

        try:
            verifyObject(IHost, dest_host)
        except BrokenImplementation:
            logging.fatal('%r doesn\'t implement IHost correct.', dest_host)
            return 1

        repo = args['name']
        if len(dest_split) > 1:
            repo = dest_split[1]

        url = dest_host.create_project(args['source'], repo)
        if url == False:
            return 1

        dest = url
        logging.info('Destination URL is: "%s".' % url)

    if get_url_host(dest) is None:
        logging.fatal('No repository handler for destination URL "%s" found.' % dest)
        return 1

    repo_cfg = {
        'source': args['source'],
        'dest': dest,
        'force': args['force'],
        'prune': args['prune'],
    }

    config['repos'][args['name']] = repo_cfg

    return 0
