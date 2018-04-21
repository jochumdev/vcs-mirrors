import argparse
import os
import sys
import logging

from vcs_mirrors.lib.config import load_config
from vcs_mirrors.lib.config import save_config
from vcs_mirrors.lib.loader import load_commands


DEFAULT_CONFIG_FILE = os.getenv('VCS_MIRROR_CONFIG', 'vcs-mirrors.yaml')
DEFAULT_LOG_LEVEL = logging.INFO
DEFAULT_LOG_FORMAT = '%(levelname)-8.8s  %(message)s'


def main(args=None):
    """The main routine."""
    if args is None:
        args = sys.argv[1:]

    parser = argparse.ArgumentParser(
        description='vcs-mirror Command-Line Interface')

    subparsers = parser.add_subparsers(title='subcommands',
                                       description='Main vcs-mirror CLI commands',
                                       dest='subcommand',
                                       help='Choose and run with --help')
    subparsers.required = True

    cmds = load_commands()

    for name, cmd in cmds.items():
        subparser = subparsers.add_parser(name)
        subparser.set_defaults(which=name)

        subparser.add_argument('--config',
                               help='Application configuration file',
                               dest='yaml_file',
                               required=False,
                               default=DEFAULT_CONFIG_FILE)

        subparser.add_argument('-q', '--quiet', action='store_const',
                               const=logging.CRITICAL, dest='verbosity',
                               help='Show only critical errors.')

        subparser.add_argument('-v', '--debug', action='store_const',
                               const=logging.DEBUG, dest='verbosity',
                               help='Show all messages, including debug messages.')

        cmd.configure_argparse(subparser)


    # Parse command-line arguments
    parsed_args = vars(parser.parse_args(args))

    # Initialize logging from
    level = parsed_args.get('verbosity') or DEFAULT_LOG_LEVEL
    logging.basicConfig(level=level, format=DEFAULT_LOG_FORMAT)

    config = load_config(parsed_args['yaml_file'])
    if config['repos'] is None:
        config['repos'] = {}

    # Execute the command
    which_command = parsed_args['which']
    result = cmds[which_command].execute(config, parsed_args)
    if result != 0:
        sys.exit(result)

    save_config(config, parsed_args['yaml_file'])
