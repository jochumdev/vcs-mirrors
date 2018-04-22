import logging
import os
import os.path
import re
import shlex
import subprocess

from zope.interface import implementer

from vcs_mirrors.lib.cd import Cd
from vcs_mirrors.lib.interfaces import IRepo
from vcs_mirrors.lib.utils import run_cmd

__all__ = ['Repo']


@implementer(IRepo)
class Repo(object):
    TYPE = 'git'

    @staticmethod
    def get_host(url):
        """
        Returns the hostname when the url is a git host else None

        Tested urls:
            - https://github.com/pcdummy/vcs-mirrors.git
            - https://git.lxch.eu/vcs-mirrors.git
            - ssh://user@server/project.git
            - user@server:project.git
            - git://git.proxmox.com/git/aab.git
        """
        url = str(url)

        # https://github.com/pcdummy/vcs-mirrors.git
        # https://git.lxch.eu/vcs-mirrors.git
        match = re.search(r'https://([-\d\w_\.]+)/.*\.git$', url)
        if match:
            return match.group(1)

        # ssh://user@server/project.git
        match = re.search(
            r'(ssh://)?[-\d\w_\.]+@{1}([-\d\w_\.]+)[:/]{1}.*\.git$', url)
        if match:
            return match.group(2)

        # git://git.lxch.eu/git/aab.git
        match = re.search(r'git://([-\d\w_\.]+)/.*\.git$', url)
        if match:
            return match.group(1)

        return None

    _config = None

    def _after_clone(self):
        pass

    def __init__(self, config):
        self._config = config

    def fetch(self, repo):
        logging.debug('%s: Fetching repository "%s"' % (self, repo))

        repo_config = self._config['repos'][repo]
        force = False
        if 'force' in repo_config:
            force = repo_config['force']

        prune = False
        if 'prune' in repo_config:
            prune = repo_config['prune']

        repo_dir = os.path.join(self._config['settings']['local_path'], repo)
        repo_dir_exists = True
        if not os.path.exists(repo_dir):
            repo_dir_exists = False
            logging.debug('%s: Makedirs: "%s"' % (self, repo_dir))
            os.makedirs(repo_dir, mode=0o700)

        logging.debug('%s: cd %s' % (self, os.path.abspath(repo_dir)))
        with Cd(repo_dir):
            if not repo_dir_exists:
                run_cmd(['git', 'clone', '--mirror', shlex.quote(repo_config['source']), '.'])
                #run_cmd(['git', 'remote', 'rename', 'origin', 'source'])
                self._after_clone()
            else:
                has_repo = run_cmd(['git', 'remote', 'get-url', 'origin'], False).returncode == 0
                if not has_repo:
                    run_cmd(['git', 'remote', 'add', 'origin', shlex.quote(repo_config['source'])])

                args = ['git', 'fetch']
                if force:
                    args.append('--force')
                if prune:
                    args.append('--prune')
                args.append('origin')

                run_cmd(args)

        return True

    def push(self, repo):
        logging.debug('%s: Pushing to repository "%s"' % (self, repo))

        repo_dir = os.path.join(self._config['settings']['local_path'], repo)
        if not os.path.exists(repo_dir):
            logging.error('%s: Can\'t push repo "%s", it does not exists localy.' % (self, repo))

        repo_config = self._config['repos'][repo]
        force = False
        if 'force' in repo_config:
            force = repo_config['force']

        prune = False
        if 'prune' in repo_config:
            prune = repo_config['prune']

        with Cd(repo_dir):
            has_repo = run_cmd(['git', 'remote', 'get-url', 'dest'], False).returncode == 0
            if not has_repo:
                run_cmd(['git', 'remote', 'add', 'dest', shlex.quote(repo_config['dest'])])
                run_cmd(['git', 'config', '--add', 'remote.dest.push', "+refs/heads/*:refs/heads/*"])
                run_cmd(['git', 'config', '--add', 'remote.dest.push', "+refs/tags/*:refs/tags/*"])
                run_cmd(['git', 'config', 'remote.dest.mirror', 'true'])

                if repo_config['dest'][0:4] == 'http':
                    run_cmd(['git', 'config', 'credential.helper', 'store'])

            args = ['git', 'push']
            if force:
                args.append('--force')
            if prune:
                args.append('--prune')
            args.extend(['dest'])

            run_cmd(args)

        return True

    def __str__(self):
        return self.TYPE

    def __repr__(self):
        return '<repo(%s)>' % self.TYPE
