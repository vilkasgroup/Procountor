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

Installation
------------

::

    pip install Procountor

Usage
-----

Create a client and call the API. The client fetches an access token on
construction, so creating it requires valid credentials.

.. code-block:: python

    from procountor import Client

    client = Client(
        api_key="your-api-key",
        client_id="your-client-id",
        client_secret="your-client-secret",
        redirect_uri="https://your-app.example.com/callback",
        test_mode=True,          # talk to the Procountor test API
        api_version="supported",  # "supported", "latest" or a dated version e.g. "26.05"
    )

    # Every method returns a dict with a "status" key and, on success, "content".
    response = client.get_invoices(startDate="2024-01-01", endDate="2024-01-31")
    if response["status"] == 200:
        for invoice in response["content"]["results"]:
            print(invoice["id"])

    # Fetch a single invoice
    invoice = client.get_invoice(8204221)

Calling any endpoint
--------------------

The Procountor API is large and this library ships named helpers for only a
subset of it. The client's main job is authentication and token refresh -- once
you have a client you can reach **any** endpoint with the generic verbs, no
dedicated method required:

.. code-block:: python

    # GET with query parameters
    client.get("payrolls/salaryslips", salaryPeriodId=123)

    # POST / PUT with a JSON body (dict or list)
    client.post("products", json={"name": "Widget", "type": "PURCHASE"})
    client.put("invoices/8204221/notes", json={"note": "Checked"})

    # DELETE
    client.delete("attachments/42")

Endpoint paths are relative to the API version base URL (e.g. ``invoices`` or
``invoices/8204221``). See the official Procountor developer documentation at
https://dev.procountor.com/ for the full list of endpoints and their payloads.

API versions
------------

The ``api_version`` argument selects which Procountor API version the client
talks to:

* ``"supported"`` -- updated to the latest numbered version every three months.
  Stable and recommended for production integrations. (Default.)
* ``"latest"`` -- a monthly release with no extended support; may change from
  month to month.
* A dated version such as ``"26.05"`` -- a specific release snapshot. Procountor
  keeps a handful of recent dated versions available, each supported for roughly
  nine months, so pinning one gives you a predictable upgrade window.

See https://dev.procountor.com/release-notes/ for the current release schedule
and which dated versions are available.

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

Push the commit and the new tag together::

    git push --follow-tags

Pushing a ``v*`` tag triggers the publish workflow. Double check that the
GitHub Action runs successfully.