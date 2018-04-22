.. image:: https://badge.fury.io/py/vcs-mirrors.svg
   :target: https://badge.fury.io/py/vcs-mirrors

.. image:: https://img.shields.io/pypi/pyversions/vcs-mirrors.svg
   :target: https://pypi.python.org/pypi/vcs-mirrors

vcs-mirrors
===========

A python-only clone of https://github.com/samrocketman/gitlab-mirrors/ with a YAML config file.

Requirements
------------

- Python 3.5+ (Debian Stretch+, Ubuntu Xenial+)
- virtualenv if you don't want to mess with System Python
- git-remote-bzr https://github.com/felipec/git-remote-bzr for Bazaar support

Features
--------

* Mirror different types of source repositories: Bazaar, Git, Subversion. Mirror all into git.
* GitLab mirror adding.
    * When adding a mirror if the project doesn't exist in GitLab it will be auto-created.
    * Set project creation defaults (e.g. issues enabled, wiki enabled, etc.)
* Github mirror adding.
    * Same as with Gitlab.
* mirror anything to Git (not just Gitlab and Github).
* Update a single mirror.
* Update all known mirrors.


Installation
++++++++++++

On Debian
---------

For Bazaar support:

.. code:: bash

    $ apt install git-remote-bzr

Install into a virtualenv:

.. code:: bash

    $ virtualenv -p /usr/bin/python3 --no-site-packages venv
    $ venv/bin/pip install "vcs-mirrors[gitlab,github]"

Then copy vcs-mirrors.yaml.example into your current-working-directory:

.. code:: bash

    $ cp venv/lib/python3.6/site-packages/vcs-mirrors/vcs-mirrors.yaml.sample vcs-mirrors.yaml

Edit it for your needs.

Usage
+++++
.. code:: bash

    venv/bin/vcs-mirrors -h
    venv/bin/vcs-mirrors add -h

add examples:
-------------

This one try to create a repo "pcdummy/proxmox-dockerfiles" on git.lxch.eu - the identifier must be unique in the config file:

.. code:: bash

   $ vcs-mirrors add me/p-dockerfiles https://github.com/pcdummy/proxmox-dockerfiles.git git.lxch.eu:pcdummy/proxmox-dockerfiles


This doesn't:

.. code:: bash

    $ vcs-mirrors add me/p-dockerfiles https://github.com/pcdummy/proxmox-dockerfiles.git git@git.lxch.eu:pcdummy/proxmox-dockerfiles.git

Full mirroring include "prune" and "force" pull/push:

.. code:: bash

    $ vcs-mirrors add -f -p me/p-dockerfiles https://github.com/pcdummy/proxmox-dockerfiles.git git.lxch.eu:pcdummy/proxmox-dockerfiles

If you give an host as target "add" creates the repo on the host and translates it to a git URL else add does nothing else than adding the params to your configuration file.


Development
+++++++++++

.. code:: bash

    $ pip install -e ."[development,gitlab,github]"


Keywords
++++++++

gitlab github sync mirror vcs-mirror bazaar