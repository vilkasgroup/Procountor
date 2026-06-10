===================
Procountor
===================

.. image:: https://github.com/vilkasgroup/Procountor/actions/workflows/ci.yml/badge.svg
   :target: https://github.com/vilkasgroup/Procountor/actions/workflows/ci.yml
   :alt: CI status

.. image:: https://readthedocs.org/projects/procountor/badge/?version=latest
   :target: https://procountor.readthedocs.io/en/latest/?badge=latest
   :alt: Documentation Status


Python library for calling Procountor services

* Free software: MIT license
* Documentation: https://procountor.readthedocs.io.


Features
--------

* Full client for calling Procountor REST API

Credits
---------

This package was created with Cookiecutter_ and the `audreyr/cookiecutter-pypackage`_ project template.

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`audreyr/cookiecutter-pypackage`: https://github.com/audreyr/cookiecutter-pypackage


Development
-----------

This project uses `uv <https://docs.astral.sh/uv/>`_ for dependency and
environment management.

Set up the environment and run the test suite::

    uv sync
    uv run pytest
    uv run ruff check procountor tests

The unit tests run fully offline. The live integration tests against the
Procountor test API are skipped unless you opt in by exporting the
``PROCOUNTOR_*`` credentials and ``PROCOUNTOR_RUN_INTEGRATION=1``::

    export PROCOUNTOR_RUN_INTEGRATION=1
    export PROCOUNTOR_API_KEY=...
    export PROCOUNTOR_CLIENT_ID=...
    export PROCOUNTOR_CLIENT_SECRET=...
    export PROCOUNTOR_REDIRECT_URI=...
    export PROCOUNTOR_API_VERSION=...
    uv run pytest


Releasing a new version to PyPI
-------------------------------

Update ``HISTORY.rst`` and commit the changes.

Bump the version (``patch`` | ``minor`` | ``major`` depending on the scale of
changes)::

    uv run bump-my-version bump patch

Push the changes and the new tag::

    git push
    git push --tags

Pushing a ``v*`` tag triggers the publish workflow. Double check that the
GitHub Action runs successfully.