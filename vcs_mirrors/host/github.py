import logging

from zope.interface import implementer

from vcs_mirrors.lib.interfaces import IHost

try:
    from github import Github
    from github.GithubException import GithubException
    from github.GithubException import UnknownObjectException
    GITHUB_AVAILABLE = True
except ImportError:
    GITHUB_AVAILABLE = False
    pass

__all__ = ['__virtual__', 'Host']


def __virtual__():
    if not GITHUB_AVAILABLE:
        logging.warn(
            'Host type "github" isn\'t available, couldn\'t import pygithub')
    return GITHUB_AVAILABLE


@implementer(IHost)
class Host(object):

    TYPE = 'github'

    _settings = None

    def __init__(self, host, settings):
        self._settings = {
            'public': True,
            'issues_enabled': True,
            'wiki_enabled': True,
            'downloads_enabled': True,
            'projects_enabled': True,
            'use_https': False,
        }

        self._settings.update(settings)

        self._api = Github(self._settings['api_key'])

    def create_project(self, source, repo):
        desc = 'Git mirror of %s.' % source
        if self._settings['public']:
            desc = 'Public mirror of %s' % source

        org, name = repo.split('/')
        g_user = self._api.get_user()

        logging.info('%s: Createing project: "%s"' % (self, repo))
        g_repo = None
        if org == g_user.login:
            try:
                g_repo = g_user.create_repo(
                    name,
                    description=desc,
                    private=not self._settings['public'],
                    has_issues=self._settings['issues_enabled'],
                    has_wiki=self._settings['wiki_enabled'],
                    has_downloads=self._settings['downloads_enabled'],
                    has_projects=self._settings['projects_enabled'],
                )
            except GithubException:
                return False

        else:
            # Find org
            try:
                g_org = self._api.get_organization(org)
            except UnknownObjectException:
                return False

            # Create repo
            try:
                g_repo = g_org.create_repo(
                    name,
                    description=desc,
                    private=not self._settings['public'],
                    has_issues=self._settings['issues_enabled'],
                    has_wiki=self._settings['wiki_enabled'],
                    has_downloads=self._settings['downloads_enabled'],
                    has_projects=self._settings['projects_enabled'],
                )
            except GithubException:
                return False

        if self._settings['use_https']:
            return g_repo.clone_url

        return g_repo.ssh_url

    def get_url(self, repo):
        g_repo = self._api.get_repo(repo)

        if self._settings['use_https']:
            return g_repo.clone_url

        return g_repo.ssh_url

    def __repr__(self):
        return '<%s>' % self.TYPE

    def __str__(self):
        return '%s' % self.TYPE
