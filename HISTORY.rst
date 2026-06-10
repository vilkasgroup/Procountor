=======
History
=======

Unreleased
----------

* **Fixed**: eight write methods (``update_company``, ``update_user``,
  ``update_business_partner``, ``update_dimension``, ``create_dimension_item``,
  ``update_dimension_item``, ``post_payment`` and
  ``payments_direct_bank_transfers``) passed the request body into the
  ``headers`` argument, so no JSON body was ever sent. They now forward the body
  correctly. This changes what these methods send on the wire.
* Added generic ``get``, ``post``, ``put`` and ``delete`` verbs so any
  Procountor endpoint can be called without a dedicated helper (the named
  helpers cover only part of the large API surface). ``request`` now also
  accepts an explicit ``json`` body, allowing top-level JSON array payloads.
  The named helper methods are now thin wrappers over these verbs (no
  behavioural change to what they send).
* **Changed**: ``update_dimension`` now takes a ``dimensionId`` argument and
  targets ``PUT /dimensions/{dimensionId}``. The previous ``PUT /dimensions``
  endpoint was removed by Procountor (around version 25.11).
* **Deprecated**: ``pay_invoice`` and ``send_one_time_pass`` now emit a
  ``DeprecationWarning``; their endpoints no longer exist in the current
  Procountor API.
* **Fixed**: ``get_payments`` queried the ``invoices`` endpoint instead of
  ``payments``.
* **Fixed**: ``get_invoice_paymentevents`` sent its arguments as a JSON body on
  a GET request; they are query parameters (``previousId``, ``orderById``,
  ``size``, ``page``) and are now sent as such.
* **Fixed**: ``create_dimension_item``, ``update_dimension_item`` and
  ``confirm_invoice`` produced URLs with a double slash because of a leading
  slash in the endpoint path.
* Added type hints throughout the package and a ``py.typed`` marker so the
  types are exposed to downstream users. The client is now split into a
  ``BaseClient`` (HTTP transport) and the ``ApiMethods`` endpoint helpers;
  ``procountor.client.Client`` and all of its methods are unchanged.
* ``Client`` is now importable directly from the top-level package
  (``from procountor import Client``).
* Project tooling modernized:

  * Migrated packaging from ``setup.py``/``setup.cfg`` to ``pyproject.toml``
    (PEP 621, hatchling build backend) and adopted ``uv`` for dependency and
    environment management. Removed ``Pipfile``/``Pipfile.lock``,
    ``requirements.txt``, ``tox.ini`` and the dead ``.pyup.yml``.
  * Dropped Python 2 support; now requires Python 3.9+.
  * Refreshed dependencies so transitive packages (urllib3, etc.) resolve to
    current, non-vulnerable versions.
  * Added an offline unit-test suite. The live integration tests now skip by
    default and only run with ``PROCOUNTOR_RUN_INTEGRATION=1`` and credentials.
  * Added a GitHub Actions CI workflow (ruff lint + pytest matrix on Python
    3.9–3.13) and modernized the PyPI publish workflow to build with ``uv``.
  * Added the previously empty ``LICENSE`` (MIT) file.

2.5.0 (2025-07-31)
------------------

* Update client to use environment variables for endpoint hosts and updated default test url

2.3.2 (2022-06-26)
------------------

* up version number to test new release process

2.3.1 (2022-06-26)
------------------

* Don't send empty json body in get requests
  * fixes problem with azure api gateway rejecting messages
* remove travis

2.2.1 (2021-11-15)
------------------

* Better API Token error message if getting token fails

1.2.0 (2020-04-08)
------------------

* Support for new API urls
    * latest
    * supported (Default)
    * Special version >= 20.02 - not yet new functionalities.

1.1.0 (2019-06-17)
------------------

* Support to use a specified version of Procountor API

1.0.0 (2019-04-21)
------------------

* Version 1.0.0 is compatibled with Procountor API version 10.
* Returns response as dict with keys: status, message and data

0.2.1 (2018-05-24)
------------------

* Fix get_invoices and get_ledger_receipts
* Return attachment data parsed


0.2.0 (2018-05-16)
------------------

* Add an option for using the real API endpoint


0.1.0 (2018-03-15)
------------------

* Bump version: 0.0.1 -> 0.1.0


0.0.1 (2018-03-15)
------------------

* First release for PyPi
