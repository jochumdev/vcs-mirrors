"""
Large parts from: https://github.com/samrocketman/gitlab-mirrors/blob/development/lib/manage_gitlab_project.py
"""

import logging
from zope.interface import implementer

from vcs_mirrors.lib.interfaces import IHost

try:
    import gitlab
    from gitlab.exceptions import GitlabCreateError
    GITLAB_AVAILABLE = True
except ImportError:
    GITLAB_AVAILABLE = False
    pass

__all__ = ['__virtual__', 'Host']


def __virtual__():
    if not GITLAB_AVAILABLE:
        logging.warn(
            'Host type "gitlab" isn\'t available, couldn\'t import python-gitlab')
    return GITLAB_AVAILABLE


def _find_matches(objects, kwargs, find_all):
    """Helper function for _add_find_fn. Find objects whose properties
    match all key, value pairs in kwargs.
    Source: https://github.com/doctormo/python-gitlab3/blob/master/gitlab3/__init__.py
    """
    ret = []
    for obj in objects:
        match = True
        # Match all supplied parameters
        for param, val in kwargs.items():
            if not getattr(obj, param) == val:
                match = False
                break
            if match:
                if find_all:
                    ret.append(obj)
                else:
                    return obj
    if not find_all:
        return None

    return ret


@implementer(IHost)
class Host(object):

    TYPE = 'gitlab'

    _settings = None

    def __init__(self, host, settings):
        self._settings = {
            'url': host,
            'ssl_verify': True,
            'public': False,
            'issues_enabled': False,
            'wall_enabled': False,
            'merge_requests_enabled': False,
            'wiki_enabled': False,
            'snippets_enabled': False,
            'use_https': False,
        }

        self._settings.update(settings)

        # pylint: disable=E1101
        self._api = gitlab.Gitlab(
            'https://' + self._settings['url'],
            self._settings['api_key'],
            ssl_verify=self._settings['ssl_verify'],
            api_version=4
        )
        # pylint: enable=E1101
        self._api.auth()

    def _find_group(self, **kwargs):
        groups = self._api.groups.list()
        return _find_matches(groups, kwargs, False)

    def _find_user(self, **kwargs):
        users = self._api.users.list()
        return _find_matches(users, kwargs, False)

    def _find_project(self, **kwargs):
        projects = self._api.projects.list(as_list=True)
        return _find_matches(projects, kwargs, False)

    def create_project(self, source, repo):
        desc = 'Git mirror of %s.' % source
        if self._settings['public']:
            desc = 'Public mirror of %s' % source

        group, name = repo.split('/')

        group_obj = self._find_group(name=group)
        if group_obj is None:
            group_obj = self._find_user(username=group)

        if group_obj is None:
            logging.info('%s: Createing group: "%s"' % (self, group))
            try:
                group_obj = self._api.groups.create({'name': group, 'path': group})
            except GitlabCreateError:
                logging.error('Cannot create group "%s", error: path has already been taken.' % group)
                return False

        project_options = {
            'name': name,
            'description': desc,
            'issues_enabled': str(self._settings['issues_enabled']).lower(),
            'wall_enabled':  str(self._settings['wall_enabled']).lower(),
            'merge_requests_enabled':  str(self._settings['merge_requests_enabled']).lower(),
            'wiki_enabled':  str(self._settings['wiki_enabled']).lower(),
            'snippets_enabled':  str(self._settings['snippets_enabled']).lower(),
            'namespace_id': group_obj.id
        }

        logging.info('%s: Createing project: "%s"' % (self, repo))

        try:
            project = self._api.projects.create(project_options)
        except GitlabCreateError:
            logging.error('Cannot create project "%s", error: path has already been taken.' % repo)
            return False

        if self._settings['use_https']:
            return project.http_url_to_repo

        return project.ssh_url_to_repo

    def get_url(self, repo):
        project = self._find_project(name=repo)
        if project is None:
            return None

        if self._settings['use_https']:
            return project.http_url_to_repo

        return project.ssh_url_to_repo

    def __repr__(self):
        return '<%s(%s)>' % (self.TYPE, self._settings['url'])

    def __str__(self):
        return '%s:%s' % (self.TYPE, self._settings['url'])
