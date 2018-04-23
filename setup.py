import codecs
import os
from setuptools import setup, find_packages

# abspath here because setup.py may be __main__, in which case
# __file__ is not guaranteed to be absolute
here = os.path.abspath(os.path.dirname(__file__))


def read_file(filename):
    """Open a related file and return its content."""
    with codecs.open(os.path.join(here, filename), encoding='utf-8') as f:
        content = f.read()
    return content


README = read_file('README.rst')
CHANGELOG = read_file('CHANGELOG.rst')
CONTRIBUTORS = read_file('CONTRIBUTORS.rst')

REQUIREMENTS = [
    'ruamel.yaml',
    'zope.interface',
]

GITLAB_REQUIRES = [
    'python-gitlab',
]

GITHUB_REQUIRES = [
    'pygithub',
]

DEVELOPMENT_REQUIRES = [
    'pylint',
    'autopep8',
    'flake8',
    'ipython',
    'zest.releaser',
]

DEPENDENCY_LINKS = []

ENTRY_POINTS = {
    'console_scripts': [
        'vcs-mirrors = vcs_mirrors.scripts.main:main'
    ]
}

setup(name='vcs_mirrors',
      version='0.0.7',
      description='',
      long_description='{}\n\n{}\n\n{}'.format(README, CHANGELOG, CONTRIBUTORS),
      license='MIT',
      classifiers=[
          'Programming Language :: Python',
          'Programming Language :: Python :: 3',
          'Programming Language :: Python :: 3.5',
          'Programming Language :: Python :: 3.6',
          'License :: OSI Approved :: MIT License',
          'Topic :: Software Development :: Version Control',
          'Topic :: Software Development :: Version Control :: Bazaar',
          'Topic :: Software Development :: Version Control :: Git',
      ],
      keywords='Console VCS mirror vcs-mirrors',
      author='René Jochum',
      author_email='rene@jochums.at',
      url='https://git.lxch.eu/pcdummy/vcs-mirrors',
      packages=find_packages(),
      package_data={'': ['*.rst', '*.py', '*.yaml']},
      include_package_data=True,
      zip_safe=False,
      install_requires=REQUIREMENTS,
      extras_require={
          'gitlab': GITLAB_REQUIRES,
          'github': GITHUB_REQUIRES,
          'development': DEVELOPMENT_REQUIRES,
      },
      dependency_links=DEPENDENCY_LINKS,
      entry_points=ENTRY_POINTS)
