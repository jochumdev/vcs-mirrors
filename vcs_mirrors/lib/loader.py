import importlib
import pkgutil

import logging
import vcs_mirrors.command
import vcs_mirrors.host
import vcs_mirrors.repo
from vcs_mirrors.lib.interfaces import IHost, IRepo

REPOS = None
HOSTS = None
COMMANDS = None


def _load_all(package):
    """
    https://stackoverflow.com/a/1707786/3368468
    """
    result = {}
    for _, modname, ispkg in pkgutil.iter_modules(package.__path__):
        if ispkg == False:
            module = importlib.import_module(
                package.__name__ + '.' + modname, package)
            result[modname] = module
    return result


def load_commands():
    global COMMANDS
    if COMMANDS is not None:
        return COMMANDS

    COMMANDS = _load_all(vcs_mirrors.command)
    return COMMANDS


def load_repos():
    global REPOS
    if REPOS is not None:
        return REPOS

    REPOS = {}
    for k, m in _load_all(vcs_mirrors.repo).items():
        # pylint: disable=E1120
        if IRepo.implementedBy(m.Repo):
            REPOS[k] = m.Repo
        else:
            logging.error('Repo "%s" doesn\'t implement IRepo' % k)
        # pylint: enable=E1120

    return REPOS


def load_hosts():
    global HOSTS
    if HOSTS is not None:
        return HOSTS

    HOSTS = {}
    for k, m in _load_all(vcs_mirrors.host).items():
        if not m.__virtual__():
            continue

        # pylint: disable=E1120
        if IHost.implementedBy(m.Host):
            HOSTS[k] = m.Host
        else:
            logging.error('Host "%s" doesn\'t implement IHost' % k)
        # pylint: enable=E1120

    return HOSTS
