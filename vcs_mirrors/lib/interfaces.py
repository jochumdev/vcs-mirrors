from zope.interface import Attribute, Interface


# pylint: disable=E0239,E0213
class IHost(Interface):
    """
    Host interface, all Hosts MUST implement this
    """

    TYPE = Attribute("""Type of the Host (normaly lowercase of module name)""")

    def create_project(source, repo):
        """
        Create the repo "repo" on the host
        Returns the URL for the created project or False on error.

        :return: url or False
        """

    def get_url(repo):
        """
        Returns the URL for the given repo
        and None if not found.

        :return: url or None
        """


class IRepo(Interface):
    """
    Repo interface, all Repos MUST implement this
    """

    TYPE = Attribute("""Type of the Repo (normaly lowercase of module name)""")

    def fetch(repo):
        """
        Mirrors the source url to the internal store.

        :param repo: Internal repo name
        :return: boolean
        """

    def push(repo):
        """
        Push from the internal store to the destination.

        :param repo: Internal repo name
        :return: boolean
        """
# pylint: enable=E0239,E0213
