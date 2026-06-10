from __future__ import annotations

import json
import warnings
from typing import Any

from .transport import BaseClient, ResponseDict


class ApiMethods(BaseClient):
    """High-level helpers for the Procountor REST API endpoints.

    Builds on :class:`procountor.transport.BaseClient`, which provides the HTTP
    transport and authentication used by every method here.
    """

    # Attachments
    def get_attachment(self, attachmentId: int) -> ResponseDict:
        """Gets and returns an attachment based on given attachment ID. Both attachment metadata (application/json) and
        the file itself will be returned. Content-type for the r is multipart/mixed.

        :param attachmentId: ID of the requested attachment, integer
        :return: Dictionary with keys: 'status' for HTTP-status code and 'content' for the file itself, dict
        """

        method = "GET"
        endpoint = "attachments/{}".format(attachmentId)

        return self.request(method, endpoint)

    def delete_attachment(self, attachmentId: int) -> ResponseDict:
        """Deletes requested attachment

        :param attachmentId: ID of the requested attachment to delete, integer
        :return: Dictionary with key: status, dict
        """

        method = "DELETE"
        endpoint = "attachments/{}".format(attachmentId)

        return self.request(method, endpoint)

    def post_attachment(self, meta: dict[str, Any], filename: str) -> ResponseDict:
        """Method sends new attachment to Procountor. The attachment can be of any type but limited to max 10000000
        bytes (10MB). Content-type for the request is multipart/form-data. Type for the meta data is application/json.

        :param meta: meta data for attachment, contains name of the file, referenceType and referenceId of the
                     attachment, dict
        :param filename: path to the file
        :return: Dictionary with request status code ['status'] and ['content']  content of the request
        """

        method = "POST"
        endpoint = "attachments"

        with open(filename, "rb") as f:
            files = {
                'meta': (None, json.dumps(meta), "application/json"),
                'file': f.read(),
            }

            return self.request(method, endpoint, files=files, headers=self._headers(method, endpoint))

    # Bank accounts
    def get_bank_accounts(self, **kwargs: Any) -> ResponseDict:
        """Method returns the bank accounts for the current environment.

        :param previousId: Previous bank account ID for pagination. If this field is set and results are ordered by order number, value has to an identifier of existing bank account in the given company.
        :param orderById: Order the results by bank account ID
        :param orderByOrderNo: Order the results by bank account order number
        :param size: Page size for the results
        :return: Dictionary with request status code ['status'] and ['content'] content of the request
        """
        method = "GET"
        endpoint = self._create_endpoint("bankaccounts", kwargs)

        return self.request(method, endpoint)

    # BANK STATEMENTS
    def get_bank_statements(self, startDate: str, endDate: str) -> ResponseDict:
        """Gets and returns all bank statements that match the request criteria. Each BankStatementEvent can have a
        list of child events. In that case, the event model contains an additional "event" property with an array of
        BankStatementEvents as its value.

        :param startDate: Start date of the search (yyyy-MM-dd), string
        :param endDate: End date of the search (yyyy-MM-dd), string
        :return: Dictionary with keys: status and content, dict
        """
        dates = {
            'startDate': startDate,
            'endDate': endDate,
        }
        method = "GET"
        endpoint = self._create_endpoint("bankstatements", dates)

        return self.request(method, endpoint)

    def delete_products_from_bank_statement(self, statementId: int, eventId: int) -> ResponseDict:
        """Method deletes allocation of a product from a bank statement event

        :param statementId: ID of the bankstatement, integer
        :param eventId: ID of the event, integer
        :return: Dictionary with key: status, dict
        """

        method = "DELETE"
        endpoint = "bankstatements/{}/events/{}/products".format(statementId, eventId)

        return self.request(method, endpoint)

    def put_products_to_bank_statement(self, statementId: int, eventId: int, **data: Any) -> ResponseDict:
        """Method allocates a product to a bank statement event

        :param statementId: ID of the bankstatement, integer
        :param eventId: ID of the event, integer
        :param **data: product information, dict
        :return: Dictionary with key: status, dict
        """

        method = "PUT"
        endpoint = "bankstatements/{}/events/{}/products".format(statementId, eventId)

        return self.request(method, endpoint, **data)

    # BUSINESS PARTNERS

    def get_business_partners(self, **kwargs: Any) -> ResponseDict:
        """Method finds business partners matching search criteria

        :param name: Business partner name
        :param codeType: Business Partner code type
        :param code: Business Partner code
        :param customerNo: Customer number
        :param mainGroup: Main group
        :param partnerGroup: Business Partner Group
        :param type: Type of business partner. Possible value: CUSTOMER, SUPPLIER, PERSON
        :param orderById: Order the results by business partner ID. Value: asc, desc.
        :param previousId: Previous partner ID for pagination
        :param active: Status of business partner. Value: true, false.
        :return: Dictionary with request status code ['status'] and ['content'] content of the request
        """

        method = "GET"
        endpoint = self._create_endpoint("businesspartners", kwargs)

        return self.request(method, endpoint)

    def get_business_partner(self, partnerId: int) -> ResponseDict:
        """Method gets and returns requested business partner with its address

        :param partnerId: business partner's identifier, integer
        :return: Dictionary with keys: status and content, dict
        """

        method = "GET"
        endpoint = "businesspartners/{}".format(partnerId)

        return self.request(method, endpoint)

    def update_business_partner(self, partnerId: int, **kwargs: Any) -> ResponseDict:
        """Update a business partner

        :param partnerId: business partner's identifier, integer
        :param body: Business partner data to update. BusinessPartner object.
        :return: Dictionary with request status code ['status'] and ['content'] content of the request
        """

        method = "PUT"
        endpoint = "businesspartners/{}".format(partnerId)

        return self.request(method, endpoint, **kwargs)

    def get_business_partner_details(self) -> ResponseDict:
        """Method gets and returns basic information on person register entry for currently logged in user.
        Includes eg. name, address and payment information

        :return: Dictionary with keys: status and content, dict
        """

        method = "GET"
        endpoint = "businesspartners/personaldetails"

        return self.request(method, endpoint)

    # CHART OF ACCOUNTS
    def get_coa(self) -> ResponseDict:
        """Method gets and returns the chart of accounts for the current environment. It can be modified on the Chart
        of accounts page in Procountor.

        :return: Dictionary with keys: status and content, dict
        """

        method = "GET"
        endpoint = "coa"

        return self.request(method, endpoint)

    # Company
    def get_company(self) -> ResponseDict:
        """Method returns basic information of the currently logged in company.

        :return: Dictionary with keys: status and content, dict
        """

        method = "GET"
        endpoint = "company"

        return self.request(method, endpoint)

    def update_company(self, **data: Any) -> ResponseDict:
        """Updates basic information of the current company.

        :param **data: Company info data to update. Company object.
        :return: Dictionary with keys: status and content, dict
        """
        method = "PUT"
        endpoint = "company"

        return self.request(method, endpoint, **data)

    # CURRENCIES
    def get_currencies(self) -> ResponseDict:
        """Gets and returns all available currencies

        :return: Dictionary with keys: status and content, dict
        """

        method = "GET"
        endpoint = "currencies"

        return self.request(method, endpoint)

    def get_currency(self) -> ResponseDict:
        """Gets and returns currency for the current company.

        :return: Dictionary with keys: status and content, dict
        """

        method = "GET"
        endpoint = "currencies/company"

        return self.request(method, endpoint)

    def get_exchange_rate(self, **kwargs: Any) -> ResponseDict:
        """Gets and returns an exchange rate for the given currency.

        :param baseCurrency: base currency for conversion, string
        :param currency: target currency for conversion, string
        :param day: day for the rate (yyyy-MM-dd), string
        :param rateType: type of the rate, string, possible values: 'PROCOUNTOR_ACCOUNTING_EXCHANGE_RATE',
                         'ACCOUNT_CURRENCY_AVERAGE_RATE', 'ACCOUNT_CURRENCY_BUYING_RATE',
                         'ACCOUNT_CURRENCY_SELLING_RATE', 'CASH_BUYING_RATE', 'CASH_CURRENCY_SALE_EXCHANGE_RATE'
        :return: Dictionary with keys: status and content, dict
        """

        method = "GET"
        endpoint = "{}{}".format("currencies/exchangerate", self._dict_to_url_query(kwargs))

        return self.request(method, endpoint)

    def get_latest_currency_rate(self, **kwargs: Any) -> ResponseDict:
        """Gets and returns list of currency rates for the company base currency

        :param rateType: requested rate type, integer, values: 1 - Procountor Accounting Exchange Rate, 2 - Average
                         Rate, 3 - Buy Rate, 4 - Sell Rate, 5 - Cash Buy Rate, 6 - Cash sale exchange rate
        :return: Dictionary with keys: status and content, dict
        """

        method = "GET"
        endpoint = self._create_endpoint("currencies/latest", kwargs)

        return self.request(method, endpoint)

    # DIMENSIONS
    def get_dimensions(self) -> ResponseDict:
        """Gets and returns a list of all dimensions and dimension items for the current company. Dimensions can be set
        on the Dimensions page in Procountor.

        :return: Dictionary with keys: status and content, dict
        """

        method = "GET"
        endpoint = "dimensions"

        return self.request(method, endpoint)

    def update_dimension(self, **kwargs: Any) -> ResponseDict:
        """Update dimension

        .. deprecated::
            This PUTs to ``/dimensions``, which the current Procountor API no
            longer accepts. Use ``PUT /dimensions/{dimensionId}`` instead, e.g.
            ``client.put("dimensions/{}".format(dimension_id), json=dimension)``.

        :param body: Dimension object

        :return: Dictionary with keys: status and content, dict
        """
        warnings.warn(
            "update_dimension targets PUT /dimensions, which no longer exists "
            "in the Procountor API. Use client.put('dimensions/<id>', json=...) "
            "instead.",
            DeprecationWarning,
            stacklevel=2,
        )

        method = "PUT"
        endpoint = "dimensions"
        return self.request(method, endpoint, **kwargs)

    def get_dimension(self, dimensionId: int) -> ResponseDict:
        """Gets and returns a specified dimension with its dimension items

        :param dimensionId: dimension identifier, integer
        :return: Dictionary with keys: status and content, dict
        """

        method = "GET"
        endpoint = "dimensions/{}".format(dimensionId)

        return self.request(method, endpoint)

    def create_dimension_item(self, dimensionId: int, **data: Any) -> ResponseDict:
        """Method create a new item for dimension

        :param **data: DimensionItem object.
        """

        method = "POST"
        endpoint = "dimensions/{}/items".format(dimensionId)

        return self.request(method, endpoint, **data)

    def update_dimension_item(self, dimensionId: int, **data: Any) -> ResponseDict:
        """Update item in dimension
        :param **data: DimensionItem object to update

        :return: Dictionary with request status code ['status'] and ['content'] content of the request
        """

        method = "PUT"
        endpoint = "dimensions/{}/items".format(dimensionId)

        return self.request(method, endpoint, **data)

    # FISCAL YEARS
    def get_fiscal_years(self) -> ResponseDict:
        """Gets and returns fiscal years ordered by their start date, from newest to oldest. Tracking periods, if
        exist, are in chronological order. Fiscal years can be edited on the Fiscal years page in Procountor.

        :return: Dictionary with keys: status and content, dict
        """

        method = "GET"
        endpoint = "fiscalyears"

        return self.request(method, endpoint)

    # INVOICES
    def get_invoices(self, **kwargs: Any) -> ResponseDict:
        """Method searches invoices. Returns a list containing basic information for the invoices. The ID in each
        result entry can be used to fetch complete invoice details with the GET /invoices/{invoiceId} endpoint,
        get_invoice() method. Supports purchase, sales, self-assessed tax, travel and expense (bill of charges)
        invoices.

        NOTE: Maximum invoices to fetch in one request is 50, so the 50th invoice's ID must be used as previousId if
        more pages are fetched. For the first fetch 0 as a previousId value is ok.

        :param status: Invoice status, string
        :param startDate: start date of the search (billing date), string (yyyy-MM-dd)
        :param endDate: end date of the search (billing date), string (yyyy-MM-dd)
        :param createdStartDate: Start date of the search (invoice created date), string (yyyy-mm-ddTHH:MM:SS)
        :param createdEndDate: End date of the search (invoice created date), string (yyyy-mm-ddTHH:MM:SS)
        :param versionStartDate: Start date of the search (invoice updated date), string (yyyy-mm-ddTHH:MM:SS)
        :param versionEndDate: End date of the search (invoice updated date), string (yyyy-mm-ddTHH:MM:SS)
        :param types: invoice types, list.
        :param businessPartnerId: Search invoices with given business partner ID, string
        :param previousId: previous invoice ID for pagination (max pagesize is 50), string.
        :param orderById: order the results by invoice ID (asc, desc), string
        :param orderByDate: order the results by date (asc, desc), string
        :param orderByCreated: Order the results by created date (asc, desc), string
        :return: Dictionary with request status code ['status'] and basic information for the invoices ['content'], dict
        """

        method = "GET"
        endpoint = self._create_endpoint("invoices", kwargs)

        return self.request(method, endpoint)

    def get_invoice(self, invoiceId: int) -> ResponseDict:
        """Method gets and returns the requested invoice. Supports expense (bill of charges), purchase,
        sales,self-assessed tax and travel invoices.

        :param invoiceId: ID of the invoice, integer
        :return: Dictionary with request status code ['status'] and request content ['content], dict
        """

        method = "GET"
        endpoint = "invoices/{}".format(invoiceId)

        return self.request(method, endpoint)

    def post_invoice(self, **data: Any) -> ResponseDict:
        """Method posts new invoice to Procountor.

        :param **data: Invoice data objects, dict
        :return: Dictionary with request status code ['status'] and request content ['content], dict
        """

        method = "POST"
        endpoint = "invoices"

        return self.request(method, endpoint, **data)

    def approve_invoice(self, invoiceId: int, **data: Any) -> ResponseDict:
        """Method approves invoice in Procountor environment. Supports purchase, travel and expense invoices. Configure
        invoice circulation settings in the Procountor environment before using this.

        :param invoiceId: ID of the invoice, integer
        :param **data: CheckingEventDTO object. Comment for verification or approval event. Max length 100., dict
        :return: Dictionary with request status code ['status'] and request content ['content], dict
        """

        method = "PUT"
        endpoint = "invoices/{}/approve".format(invoiceId)

        return self.request(method, endpoint, **data)

    def get_invoice_comment(self, invoiceId: int) -> ResponseDict:
        """
        Get invoice comments

        :return: Dictionary with request status code ['status'] and request content ['content], dict
        """
        method = "GET"
        endpoint = "invoices/{}/comments".format(invoiceId)

        return self.request(method, endpoint)

    def post_invoice_comment(self, invoiceId: int, **data: Any) -> ResponseDict:
        """
        :param invoiceId: ID of the invoice
        :param **data: CommentDTO, dict
        :return: Dictionary with key: status and content, dict
        """

        method = "POST"
        endpoint = "invoices/{}/comments".format(invoiceId)

        return self.request(method, endpoint, **data)

    def get_invoice_paymentevents(self, invoiceId: int, **data: Any) -> ResponseDict:
        """Get payment events
        :param invoiceId: Invoice identifier
        :param previousId: Previous payment event ID for pagination
        :param orderById: Order the results by payment event ID
        :param size: Page size for the results
        :return: Dictionary with key: status and content, dict
        """

        method = "GET"
        endpoint = "invoices/{}/paymentevents".format(invoiceId)

        return self.request(method, endpoint, **data)

    def delete_invoice_paymentevent(self, invoiceId: int, paymentEventId: int) -> ResponseDict:
        """Remove a payment event which is not actually related to paying through the software i.e. with the status 'marked paid'.

        :param invoiceId: Invoice identifier
        :param paymentEventId: Payment identifier
        :return: Dictionary with key: status, dict
        """
        method = "DELETE"
        endpoint = "invoices/{}/paymentevents/{}".format(invoiceId, paymentEventId)

        return self.request(method, endpoint)

    def markpaid_invoice(self, invoiceId: int, **data: Any) -> ResponseDict:
        """
        Method marks payment events as paid. Supported invoice types: SALES_INVOICE, PURCHASE_INVOICE, TRAVEL_INVOICE,
        SALARY, PERIODIC_TAX_RETURN, BILL_OF_CHARGES

        :param invoiceId: ID of the invoice, integer
        :param **data: MarkInvoiceAsPaid object, dict
        :return: request status code, integer
        """

        method = "PUT"
        endpoint = "invoices/{}/paymentevents/markpaid".format(invoiceId)

        return self.request(method, endpoint, **data)

    def send_invoice(self, invoiceId: int) -> ResponseDict:
        """Send a sales invoice to customer

        :param invoiceId: ID of the invoice, int or string
        :return: Disctionary with status code, dict
        """

        method = "PUT"
        endpoint = "invoices/{}/send".format(invoiceId)

        return self.request(method, endpoint)

    def send_invoice_to_circulation(self, invoiceId: int) -> ResponseDict:
        """Method sends requested invoice to circulation. Supports travel and expense invoices. Invoice circulation
        needs to be configured and enabled in Procountor settings. Marks invoice status as 'RECEIVED' when it is in
        'UNFINISHED' status.

        :param invoiceId: ID of the invoice, integer
        :return: Disctionary with status code, dict
        """

        method = "PUT"
        endpoint = "invoices/{}/sendToCirculation".format(str(invoiceId))

        return self.request(method, endpoint)

    def verify_invoice(self, invoiceId: int, **kwargs: Any) -> ResponseDict:
        """Method verifies invoice in Procountor environment. Supports purchase, travel and expense invoices. Configure
        invoice circulation settings in the Procountor environment before using this.

        :param invoiceId: ID of the invoice, integer
        :param comment: Comment for verification event. Max length 255, string in dict, optional
        :return: dictionary with status code, dict
        """

        method = "PUT"
        endpoint = "invoices/{}/verify".format(invoiceId)

        return self.request(method, endpoint, **kwargs)

    def confirm_invoice(self, transactionId: int) -> ResponseDict:
        """Confirm to make an action related to the given identifier

        :param transactionId:Transaction identifier to be verified before action performed
        :return: dictionary with status code, dict
        """

        method = "PUT"
        endpoint = "invoices/{}/confirm".format(transactionId)

        return self.request(method, endpoint)

    def pay_invoice(self, **data: Any) -> ResponseDict:
        """Supports purchase invoices and self-assessed tax invoices.
        All of the invoices have to be valid in order to pay.
        If paying one of the invoices fails, none of the invoices will be paid.
        A valid one time password must be supplied. The default bank account of
        the environment is used for the payment.

        .. deprecated::
            This PUTs to ``/invoices/pay``, which no longer exists in the
            current Procountor API. Use the payments endpoints instead (e.g.
            ``post_payment``).

        :param **data: Payment object, dict
        :return: dictionary with status code, dict
        """
        warnings.warn(
            "pay_invoice targets PUT /invoices/pay, which no longer exists in "
            "the Procountor API. Use the payments endpoints (e.g. post_payment) "
            "instead.",
            DeprecationWarning,
            stacklevel=2,
        )

        method = "PUT"
        endpoint = "invoices/pay"

        return self.request(method, endpoint, **data)

    # LEDGER RECEIPTS
    def get_ledger_receipts(self, **kwargs: Any) -> ResponseDict:
        """Method gets and returns a list containing basic information for the receipts. The receiptID in each result
        entry can be used to fetch complete receipt details with the GET /ledgerereceipts/{receiptId} endpoint,
        get_ledger_receipt() method. Supported ledger receipt types are journals, sales invoice ledger receipts and
        purchase ledger invoice receipts.

        :param previousId: previous ledger receipt ID for pagination, string
        :param startDate: start date of the search (yyyy-MM-dd), string
        :param endDate: end date of the search (yyyy-MM-dd), string
        :param types: ledger receipt types, list of strings, possible values: 'JOURNAL', 'PURCHASE_INVOICE',
                      'SALES_INVOICE', 'PERIODIC_TAX_RETURN'
        :param orderById: order the results by ledger receipt ID ('asc' or 'desc'), string
        :return: Dictionary with keys: status and content, dict
        """

        method = "GET"
        endpoint = self._create_endpoint("ledgerreceipts", kwargs)

        return self.request(method, endpoint)

    def get_ledger_receipt(self, receiptId: int) -> ResponseDict:
        """Method gets and returns the requested ledger receipt. Supported ledger receipt types are journals, sales
        invoice ledger receipts and purchase invoice ledger receipts

        :param receiptId: ledger receipt identifier, integer
        :return: Dictionary with keys: status and content, dict
        """

        method = "GET"
        endpoint = "ledgerreceipts/{}".format(receiptId)

        return self.request(method, endpoint)

    def post_ledger_receipt(self, **data: Any) -> ResponseDict:
        """Method sends new ledger receipt to Procountor, Supports journal type ledger receipts

        :param **data: ledger receipt data, dict
        :return: Dictionary with keys: status and content, dict
        """

        method = "POST"
        endpoint = "ledgerreceipts"

        return self.request(method, endpoint, **data)

    def update_ledger_receipt(self, receiptId: int, **data: Any) -> ResponseDict:
        """Method updates requested ledger receipt in Procountor environment. Supported ledger receipt types are
        journals, sales invoice ledger receipts and purchase invoice ledger receipts. For defining the ledger accounts,
        dimensions, VAT status or other accounting information for an invoice, use this method.

        :param receiptId: ledger receipt identifier, integer
        :param **data: ledger receipt data, dict
        :return: Dictionary with key: status, dict
        """

        method = "PUT"
        endpoint = "ledgerreceipts/{}".format(receiptId)

        return self.request(method, endpoint, **data)

    # Payments
    def get_payments(self, **kwargs: Any) -> ResponseDict:
        """Get payment transactions

        :param startDate: Start date of the search (value date)
        :param endDate: End date of the search (value date)
        :param invoiceId: Unique invoice identifier
        :param previousId: Previous payment ID for pagination
        :param orderById: Order the results by payment ID
        :return: Dictionary with keys: status and content, dict
        """

        method = "GET"
        endpoint = self._create_endpoint("payments", kwargs)

        return self.request(method, endpoint)

    def post_payment(self, **data: Any) -> ResponseDict:
        """Pay invoices
        :param **data: PaymentsList object, dict
        :return: Dictionary
        """
        method = "POST"
        endpoint = "payments"
        return self.request(method, endpoint, **data)

    def delete_payment(self, paymentId: int) -> ResponseDict:
        """Remove a payment which is not queued or paid

        :param paymentId: Payment identifier
        :return: Dictionary
        """

        method = "DELETE"
        endpoint = "payments/{}".format(paymentId)
        return self.request(method, endpoint)

    def get_payment(self, paymentId: int) -> ResponseDict:
        """Get a payment transaction

        :param paymentId: Payment identifier
        :return: Dictionary
        """
        method = "GET"
        endpoint = "payments/{}".format(paymentId)
        return self.request(method, endpoint)

    def cancel_payment(self, paymentId: int) -> ResponseDict:
        """
        :param paymentId: Payment identifier
        :return: Dictionary
        """

        method = "PUT"
        endpoint = "payments/{}/cancel".format(paymentId)
        return self.request(method, endpoint)

    def confirm_payment(self, transactionId: int) -> ResponseDict:
        """Confirmation of action with the given identifier

        :param transactionId: Transaction identifier to be verified before action performed
        :return: Dictionary
        """
        method = "PUT"
        endpoint = "payments/{}/confirm".format(transactionId)
        return self.request(method, endpoint)

    def payments_direct_bank_transfers(self, **data: Any) -> ResponseDict:
        """Creates direct bank transfers with given data

        :param data: Contains a list of direct bank transfer to be created
        :return: Dictionary
        """

        method = "POST"
        endpoint = "payments/directbanktransfers"
        return self.request(method, endpoint, **data)

    def payments_error_messages(self, **kwargs: Any) -> ResponseDict:
        """Returns all payment error messages that match the request criteria.

        :param createdStartDate: Start date of the search (value date)
        :param createdEndDate: End date of the search (value date)
        :param type: Type of error message
        :param status: Handling status of error message
        :param previousId: Previous error message ID for pagination
        :param orderById: Order the results by message ID
        :return: Dictionary
        """
        method = "GET"
        endpoint = self._create_endpoint("payments/errormessages", kwargs)
        return self.request(method, endpoint)

    # PRODUCTS
    def get_products(self, **kwargs: Any) -> ResponseDict:
        """Method gets and Returns a paginated list of products in the current environment, starting from "previousId"
        limited by "limit". Takes optional query parameters.

        :param previousId: previous invoice id for pagination, integer, optional
        :param limit: maximum number of results, defaults to 50, integer, optional
        :param group: Id of product group, list, optional
        :param type: register type of product, string, optional
        :return: Dictionary with request status code ['status'] and the list of all products ['content'], dict
        """

        method = "GET"
        endpoint = self._create_endpoint("products", kwargs)

        return self.request(method, endpoint)

    def get_product(self, productId: int) -> ResponseDict:
        """Method gets and returns the requested product based on the productId

        :param productId: wanted product's Id, integer
        :return: Disctionary with request status code ['status'] and information of wanted product ['content'], dict
        """

        method = "GET"
        endpoint = "products/{}".format(productId)

        return self.request(method, endpoint)

    def get_product_groups(self, **kwargs: Any) -> ResponseDict:
        """Method gets and returns product groups by product type

        :param productType: Product type, string
        :return: Dictionary with request status code 'status' and list of product groups 'content', dict
        """

        method = "GET"
        endpoint = self._create_endpoint("products/groups", kwargs)

        return self.request(method, endpoint)

    # Reference payments
    def get_reference_payments(self, **kwargs: Any) -> ResponseDict:
        """Returns all reference payments that match the request criteria.

        :param accountNumber: The bank account number to use when searching for related reference payments
        :param startDate: Start date of the search (value date)
        :param endDate: End date of the search (value date)
        :param previousId: Previous payment ID for pagination
        :param orderById: Order the results by payment ID
        :return: Dictionary with request status code 'status' and 'content', dict
        """

        method = "GET"
        endpoint = self._create_endpoint("referencepayments", kwargs)

        return self.request(method, endpoint)

    # Session Information
    def get_session_info(self) -> ResponseDict:
        """Returns basic information about the current session.

        :return: Dictionary with keys: status and content, dict
        """

        method = "GET"
        endpoint = "sessioninfo"

        return self.request(method, endpoint)

    # USERS
    def get_users(self) -> ResponseDict:
        """Method returns details of the currently logged in user based on the access token

        :return: Dictionary with request status code (key: status) and user information (key: content), dict
        """

        method = "GET"
        endpoint = "users"

        return self.request(method, endpoint)

    def update_user(self, **data: Any) -> ResponseDict:
        """Update user data. Input: User user object

        :param **data: User object, dict
        :return: Dictionary with keys: status and content, dict
        """
        method = "PUT"
        endpoint = "users"

        return self.request(method, endpoint, **data)

    def user_transaction_confirm(self, transactionId: int) -> ResponseDict:
        """Confirm to make an action related to the given identifier

        :param transactionId: Transaction identifier to be verified before action performed
        :return: Dictionary with keys: status and content, dict
        """

        method = "PUT"
        endpoint = "users/{}/confirm".format(transactionId)

        return self.request(method, endpoint)

    def send_one_time_pass(self) -> ResponseDict:
        """Sends a one time password for current user via SMS

        .. deprecated::
            This GETs ``/users/otp``, which no longer exists in the current
            Procountor API. One-time passwords are now handled through the MFA
            flow (see the ``/mfatransactionresult/{transactionIdentifier}``
            endpoint).

        :return: Dictionary with status key
        """
        warnings.warn(
            "send_one_time_pass targets GET /users/otp, which no longer exists "
            "in the Procountor API. One-time passwords are now handled via the "
            "MFA flow (see /mfatransactionresult).",
            DeprecationWarning,
            stacklevel=2,
        )

        method = "GET"
        endpoint = "users/otp"

        return self.request(method, endpoint)

    def get_user_profile(self, userId: int) -> ResponseDict:
        """Method gets a user profile based on the given user ID

        :param userId: requested user's ID, integer
        :return: Dictionary with  status and content keys
        """

        method = "GET"
        endpoint = "users/profiles/{}".format(userId)

        return self.request(method, endpoint)

    # VATs
    def get_vats(self) -> ResponseDict:
        """Method gets and returns VAT percentages for the current company

        :return: Dictionary with status and content keys.
        """

        method = "GET"
        endpoint = "vats/default"

        return self.request(method, endpoint)

    def get_vats_country(self, **kwargs: Any) -> ResponseDict:
        """Method gets and returns VAT percentages available for the given country

        :param countryCode: ISO 3166-1 alpha-2 format, string
        :return: Dictionary with status and content keys.
        """

        method = "GET"
        endpoint = self._create_endpoint("vats/country", kwargs)

        return self.request(method, endpoint)
