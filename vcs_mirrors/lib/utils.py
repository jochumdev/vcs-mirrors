import logging
import subprocess

from vcs_mirrors.lib.loader import load_repos


def get_url_host(url):
    repos = load_repos()

    for repo in repos.values():
        host = repo.get_host(url)
        if host is not None:
            return host

    return None


def get_repo_for_url(url, config):
    repos = load_repos()

    result = None
    for repo in repos.values():
        host = repo.get_host(url)
        if host is not None:
            result = repo(config)
            break

    return result


def sync_one(name, config):
    if name not in config['repos']:
        logging.fatal('Unknown repository "%s" given.' % name)
        return False

    repo_config = config['repos'][name]

    source_repo = get_repo_for_url(repo_config['source'], config)
    if source_repo is None:
        logging.fatal(
            'No repository handler for source URL "%s" found.' % repo_config['source'])
        return False

    dest_repo = get_repo_for_url(repo_config['dest'], config)
    if dest_repo is None:
        logging.fatal(
            'No repository handler for source URL "%s" found.' % repo_config['dest'])
        return False

    if source_repo.fetch(name) == False:
        return False

    if dest_repo.push(name) == False:
        return False

    return True

def run_cmd(args, log_error=True):
    logging.debug('Run: %s' % " ".join(args))
    result = subprocess.run(args, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    if log_error:
        if result.returncode != 0:
            logging.error(result.stderr.decode('unicode_escape'))
    return result
