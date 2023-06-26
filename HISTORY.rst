=======
History
=======

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
