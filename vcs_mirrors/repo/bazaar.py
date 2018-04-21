import re

from vcs_mirrors.lib.utils import run_cmd
from vcs_mirrors.repo.git import Repo as GitRepo


class Repo(GitRepo):
    TYPE = 'bazaar'

    @staticmethod
    def get_host(url):
        """
        Returns the hostname when the url is a git host else None

        Tested urls:
            - bzr::bzr://bzr.savannah.gnu.org/emacs/trunk
            - bzr::bzr://bzr.savannah.gnu.org/emacs
            - bzr::lp:ubuntu/hello
            - bzr::lp:bzr
            - bzr::sftp://bill@mary-laptop/cool-repo/cool-trunk
        """
        url = str(url).lower()
        match = re.search(r'bzr::([-\d\w_\.]+):(//)?([\-0-9a-z_\.]+@+)?([\-0-9a-z_\.]+)(/.+)?', url)
        if match:
            if match.group(1) == 'lp':
                return 'lp'
            else:
                return match.group(2)

        return None

    def _after_clone(self):
        run_cmd(['git', 'gc', '--aggressive'])

        super()._after_clone()
