===================
Procountor
===================

.. image:: https://img.shields.io/travis/vilkasgroup/Procountor.svg
   :target: https://travis-ci.org/vilkasgroup/Procountor
   :alt: Build status on travis

.. image:: https://readthedocs.org/projects/procountor/badge/?version=latest
   :target: https://procountor.readthedocs.io/en/latest/?badge=latest
   :alt: Documentation Status

.. image:: https://pyup.io/repos/github/vilkasgroup/Procountor/shield.svg
   :target: https://pyup.io/repos/github/vilkasgroup/Procountor/
   :alt: Updates status

.. image:: https://coveralls.io/repos/github/vilkasgroup/Procountor/badge.svg?branch=master
   :target: https://coveralls.io/github/vilkasgroup/Procountor?branch=master
   :alt: Coveralls status


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


Releasing new version to pypi
---------

Install dev tools

```
pipenv install --dev
```

Update `HISTORY.rst` and commit the changes.

Bump version. (patch | minor | major depending on the scale of changes)

```
bumpversion patch
```

Push changes and tags.

```
git push
git push --tags
```

Double check that the github action runs successfully.