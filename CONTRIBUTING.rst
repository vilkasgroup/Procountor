.. highlight:: shell

============
Contributing
============

Contributions are welcome, and they are greatly appreciated! Every
little bit helps, and credit will always be given.

You can contribute in many ways:

Types of Contributions
----------------------

Report Bugs
~~~~~~~~~~~

Report bugs at https://github.com/vilkasgroup/Procountor/issues.

If you are reporting a bug, please include:

* Your operating system name and version.
* Any details about your local setup that might be helpful in troubleshooting.
* Detailed steps to reproduce the bug.

Fix Bugs
~~~~~~~~

Look through the GitHub issues for bugs. Anything tagged with "bug"
and "help wanted" is open to whoever wants to implement it.

Implement Features
~~~~~~~~~~~~~~~~~~

Look through the GitHub issues for features. Anything tagged with "enhancement"
and "help wanted" is open to whoever wants to implement it.

Write Documentation
~~~~~~~~~~~~~~~~~~~

Procountor could always use more documentation, whether as part of the
official Procountor docs, in docstrings, or even on the web in blog posts,
articles, and such.

Submit Feedback
~~~~~~~~~~~~~~~

The best way to send feedback is to file an issue at https://github.com/vilkasgroup/Procountor/issues.

If you are proposing a feature:

* Explain in detail how it would work.
* Keep the scope as narrow as possible, to make it easier to implement.
* Remember that this is a volunteer-driven project, and that contributions
  are welcome :)

Get Started!
------------

Ready to contribute? Here's how to set up `Procountor` for local development.

1. Fork the `Procountor` repo on GitHub.
2. Clone your fork locally::

    $ git clone git@github.com:vilkasgroup/Procountor.git

3. Install your local copy with `uv <https://docs.astral.sh/uv/>`_, which
   creates the virtual environment for you::

    $ cd Procountor/
    $ uv sync

4. Create a branch for local development::

    $ git checkout -b name-of-your-bugfix-or-feature

   Now you can make your changes locally.

5. When you're done making changes, check that your changes pass the linter and
   the tests::

    $ uv run ruff check procountor tests
    $ uv run pytest

6. Commit your changes and push your branch to GitHub::

    $ git add .
    $ git commit -m "Your detailed description of your changes."
    $ git push origin name-of-your-bugfix-or-feature

7. Submit a pull request through the GitHub website.

Pull Request Guidelines
-----------------------

Before you submit a pull request, check that it meets these guidelines:

1. The pull request should include tests.
2. If the pull request adds functionality, the docs should be updated. Put
   your new functionality into a function with a docstring, and add the
   feature to the list in README.rst.
3. The pull request should work for all supported Python versions (3.9+).
   The GitHub Actions CI workflow runs the linter and the test matrix on every
   pull request; make sure it is green.

Tips
----

To run a subset of tests::

    $ uv run pytest tests/test_900_unit_client.py


Releasing new version
---------------------

When you are ready to release a new version follow these steps:

1. Merge all changes that should be included in the new release to master.
   And checkout master.
2. Update HISTORY.rst with the new version number and changes. And commit your
   changes to master.
3. run::

    $ uv run bump-my-version bump patch|minor|major

4. push to master with tags to trigger the publish workflow::

    $ git push --tags
    $ git push

The GitHub Action will build the tag and, when successful, deploy to PyPI.
