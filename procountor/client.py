import requests
import os
import json
import base64
from urllib.parse import urlparse, parse_qs
import logging
logging.basicConfig()
logging.getLogger().setLevel(logging.DEBUG)
requests_log = logging.getLogger("requests.packages.urllib3")
requests_log.setLevel(logging.DEBUG)
requests_log.propagate = True


class Client():
    """Class for Procountor accounting API

    Following packages need to be installed:
     - requests

    :param username: Procountor username, string
    :param password: Procountor password, string
    :param company_id: Procountor environment company id, string
    :param client_id: Procountor REST API client id, string
    :param client_secret: Procountor REST API client secret, string
    :param redirect_uri: URI where redirected after authentication, string
    """

    auth_url = "https://api-test.procountor.com/api/oauth/authz/"
    token_url = "https://api-test.procountor.com/api/oauth/token/"
    api_url = "https://api-test.procountor.com/api/"

    def __init__(self, username, password, company_id, client_id, client_secret, redirect_uri, access_token, refresh_token):
        self.username = username
        self.password = password
        self.company_id = company_id
        self.client_id = client_id
        self.client_secret = client_secret
        self.redirect_uri = redirect_uri
        self.access_token = access_token
        self.refresh_token = refresh_token


    def invalidate_token(self):

        headers = {
            'authorization': 'Bearer ' + self.access_token
        }

        r = requests.post('https://api-test.procountor.com/logout', headers=headers)

    # def get_auth_code(self):
    #     """Makes post request and returns authorization code which is used for getting access token and refresh token
    #
    #     :return: auth_code
    #     """
    #
    #     params = {
    #         'response_type': 'code',
    #         'username': self.username,
    #         'password': self.password,
    #         'company': self.company_id,
    #         'redirect_uri': self.redirect_uri,
    #     }
    #
    #     headers = {
    #         'content-type': 'application/x-www-form-urlencoded'
    #     }
    #
    #     r = requests.post(Client.auth_url + '?response_type=code&client_id=' + self.client_id + "&state=123456789", params=params, headers=headers)
    #     if r.status_code != 401:
    #         r.raise_for_status()
    #
    #     # have to get value of query parameter named 'code'
    #     self.auth_code = parse_qs(urlparse(r.url).query)['code'][0]
    #
    #     return self.auth_code
    #
    #
    # def get_tokens(self, auth_code):
    #     """Makes a request and returns access token and refresh token for coming requests. Access token is valid for 3600 seconds and has to refresh after that with refresh token. Refresh token is valid always.
    #
    #     :return: granted tokens, dict
    #     """
    #
    #     self.auth_code = auth_code
    #
    #     params = {
    #         'grant_type': 'authorization_code',
    #         'redirect_uri': self.redirect_uri,
    #         'code': self.auth_code,
    #         'client_id': self.client_id,
    #         'client_secret': self.client_secret,
    #     }
    #
    #     headers = {
    #         'content-type': 'application/x-www-form-urlencoded'
    #     }
    #
    #
    #     r = requests.post(Client.token_url, params=params, headers=headers)
    #     if r.status_code != 400:
    #         r.raise_for_status()
    #     for key, value in r.json().items():
    #         if key == 'access_token':
    #             self.access_token = value
    #         if key == 'refresh_token':
    #             self.refresh_token = value
    #
    #     tokens = {'access_token': self.access_token, 'refresh_token': self.refresh_token}
    #     return tokens


    def refresh_access_token(self, refresh_token):
        """If the access token is expired (3600 seconds), new access token is granted with refresh token

        :param refresh_token: token to get new access token, string
        :return: refreshed access_token, string
        """

        params = {
            'grant_type': 'refresh_token',
            'refresh_token': self.refresh_token,
            'client_id': self.client_id,
            'client_secret': self.client_secret,
        }

        headers = {
            'content-type': 'application/x-www-form-urlencoded'
        }

        r = requests.post(Client.token_url, params=params, headers=headers)
        r.raise_for_status()
        self.access_token = r.json().get('access_token')

        return self.access_token

    # USERS
    def get_users(self):
        """Method returns details of the currently logged in user based on the access token

        :return: user information, dict
        """

        method = "GET"
        endpoint = "users"

        return self.request(method, endpoint)

    def send_one_time_pass(self):
        """Sends an one time password for current user via SMS """

        method = "GET"
        endpoint = "users/otp"

        return self.request(method, endpoint)

    def get_user_profile(self, userId):
        """Method gets a user profile based on the given user ID

        :param userId: requested user's ID, integer
        :return: user profile, dict
        """

        method = "GET"
        endpoint = "users/profiles/{}".format(str(userId))

        return self.request(method, endpoint)

    # PRODUCTS
    def get_products(self, **kwargs):
        """Method gets and Returns a paginated list of products in the current environment, starting from "previousId" limited by "limit". Takes optional query parameters.

        :param previousId: previous invoice id for pagination, integer, optional
        :param limit: maximum number of results, defaults to 50, integer, optional
        :param group: Id of product group, list, optional
        :param type: register type of product, string, optional
        :return: list of all products, dict
        """

        # TODO muista paginoinnin hallinta!
        method = "GET"
        endpoint = "products"
        if kwargs is not None:
            endpoint += "?"
            index = 0
            for key, value in kwargs.items():
                index += 1
                if index < len(kwargs):
                    endpoint += "{}={}&".format(str(value))
                else:
                    endpoint += "{}={}".format(key, str(value))

        return self.request(method, endpoint)

    def get_product(self, productId):
        """Method gets and returns the requested product based on the productId

        :param productId: wanted product's Id, integer
        :return: information of wanted product, dict
        """

        method = "GET"
        endpoint = "products/{}".format(productId)

        return self.request(method, endpoint)

    def get_product_groups(self, productType):
        """Method gets and returns product groups by product type

        :param productType: Product type, string
        :return: list of product groups, list
        """

        method = "GET"
        endpoint = "products/groups?productType={}".format(productType)

        return self.request(method, endpoint)

    # VATs
    def get_vats(self):
        """Method gets and returns VAT percentages for the current company

        :return: VAT percentages, list
        """

        method = "GET"
        endpoint = "vats/default"

        return self.request(method, endpoint)

    def get_vats_coutry(self, countryCode):
        """Method gets and returns VAT percentages available for the given country

        :param countryCode: ISO 3166-1 alpha-2 format, string
        :return: VAT percentages, list
        """

        method = "GET"
        endpoint = "vats/country?countryCode={}".format(countryCode)

        return self.request(method, endpoint)

    # INVOICES
    def get_invoices(self, previousId, **kwargs):
        """Method searches invoices. Returns a list containing basic information for the invoices. The ID in each result entry can be used to fetch complete invoice details with the GET /invoices/{invoiceId} endpoint, get_invoice() method. Supports purchase, sales, self-assessed tax, travel and expense (bill of charges) invoices.

        NOTE: Maximum invoices to fetch in one request is 50, so the 50th invoice's ID must be used as previousId if more pages are fetched. For the first fetch 0 as a previousId value is ok.

        :param previousId: previous invoice ID for pagination (max pagesize is 50), string
        :param status: invoice status, string, optional
        :param startDate: start date of the search (billing date), string (yyyy-MM-dd), optional
        :param endDate: end date of the search (billing date), string (yyyy-MM-dd), optional
        :param types: invoice types, list, optional
        :param orderById: order the results by invoice ID (asc, desc), string, optional
        :param orderByDate: order the results by date (asc, desc), string, optional
        :return: basic information for the invoices, dict
        """

        method = "GET"
        endpoint = "invoices"
        if kwargs is not None:
            endpoint += "?"
            index = 0
            for key, value in kwargs.items():
                index += 1
                if index < len(kwargs):
                    endpoint += "{}={}&".format(key, str(value))
                else:
                    endpoint += "{}={}&previousId={}".format(key, str(value), str(previousId))

        return self.request(method, endpoint)

    def get_invoice(self, invoiceId):
        """Method gets and returns the requested invoice. Supports expense (bill of charges), purchase, sales,self-assessed tax and travel invoices.

        :param invoiceId: ID of the invoice, integer
        """

        method = "GET"
        endpoint = "invoices/{}".format(str(invoiceId))

        return self.request(method, endpoint)

    def post_invoice(self, **kwargs):
        """Method posts new invoice to Procountor.

        :param data: invoice data, dict
        """

        method = "POST"
        endpoint = "invoices"

        if kwargs is None:
            raise ValueError("No data given")

        return self.request(method, endpoint, **kwargs)

    def approve_invoice(self, invoiceId, **kwargs):
        """Method approves invoice in Procountor environment. Supports purchase, travel and expense invoices. Configure invoice circulation settings in the Procountor environment before using this.

        :param invoiceId: ID of the invoice, integer
        :param comment: Comment for approval event. Max length 255, string in dict, optional
        """

        method = "PUT"
        endpoint = "invoices/{}/approve".format(str(invoiceId))

        return self.request(method, endpoint, **kwargs)

    def send_invoice_to_circulation(self, invoiceId):
        """Method sends requested invoice to circulation. Supports travel and expense invoices. Invoice circulation needs to be configured and enabled in Procountor settings. Marks invoice status as 'RECEIVED' when it is in 'UNFINISHED' status.

        :param invoiceId: ID of the invoice, integer
        """

        method = "PUT"
        endpoint = "invoices/{}/sendToCirculation".format(str(invoiceId))

        return self.request(method, endpoint)

    def verify_invoice(self, invoiceId, **kwargs):
        """Method verifies invoice in Procountor environment. Supports purchase, travel and expense invoices. Configure invoice circulation settings in the Procountor environment before using this.

        :param invoiceId: ID of the invoice, integer
        :param comment: Comment for verification event. Max length 255, string in dict, optional
        """

        method = "PUT"
        endpoint = "invoices/{}/verify".format(str(invoiceId))

        return self.request(method, endpoint, **kwargs)

    def pay_invoice(self, **kwargs):
        """Method to pay invoices in Procountor. Supports purchase invoices and self-assessed tax invoices. All of the invoices have to be valid in order to pay. If paying one of the invoices fails, none of the invoices will be paid. A valid one time password must be supplied. To receive one time password, use send_one_time_pass() method. The default bank account of the environment is used for the payment.

        :param paymentData: list of payment details, list
        :param oneTimePassword: one time password (OTP) for current user, string
        """

        method = "PUT"
        endpoint = "invoices/pay"

        return self.request(method, endpoint, **kwargs)

    # CURRENCIES
    def get_currencies(self):
        """Gets and returns all available currencies

        :return: currencies, list of all available currencies, dict
        """

        method = "GET"
        endpoint = "currencies"

        return self.request(method, endpoint)

    def get_currency(self):
        """Gets and returns currency for the current company.

        :return: currency, currency for the current company, dict
        """

        method = "GET"
        endpoint = "currencies/company"

        return self.request(method, endpoint)

    def get_exchange_rate(self, **kwargs):
        """Gets and returns an exchange rate for the given currency.

        :param baseCurrency: base currency for conversion, string
        :param currency: target currency for conversion, string
        :param day: day for the rate (yyyy-MM-dd), string
        :param rateType: type of the rate, string, possible values: 'PROCOUNTOR_ACCOUNTING_EXCHANGE_RATE', 'ACCOUNT_CURRENCY_AVERAGE_RATE', 'ACCOUNT_CURRENCY_BUYING_RATE', 'ACCOUNT_CURRENCY_SELLING_RATE', 'CASH_BUYING_RATE', 'CASH_CURRENCY_SALE_EXCHANGE_RATE'
        :return: exchange rate for the given currency, dict
        """

        method = "GET"
        endpoint = "currencies/exchangerate"

        if kwargs is not None:
            endpoint += "?"
            index = 0
            for key, value in kwargs.items():
                index += 1
                if index < len(kwargs):
                    endpoint += "{}={}&".format(key, str(value))
                else:
                    endpoint += "{}={}".format(key, str(value))
        else:
            raise ValueError("No data given")

        return self.request(method, endpoint)

    def get_latest_currency_rate(self, rateType):
        """Gets and returns list of currency rates for the company base currency

        :param rateType: requested rate type, integer, values: 1 - Procountor Accounting Exchange Rate, 2 - Average Rate, 3 - Buy Rate, 4 - Sell Rate, 5 - Cash Buy Rate, 6 - Cash sale exchange rate
        :return: list of currency rates for base currency, dict
        """

        method = "GET"
        endpoint = "currencies/latest?rateType={}".format(str(rateType))

        return self.request(method, endpoint)

    # DIMENSIONS
    def get_dimensions(self):
        """Gets and returns a list of all dimensions and dimension items for the current company. Dimensios can be set on the Dimensions page in Procountor.

        :return: list of all dimensions and dimension items for the current company, dict
        """

        method = "GET"
        endpoint = "dimensions"

        return self.request(method, endpoint)

    def get_dimension(self, dimensionId):
        """Gets and returns a specified dimension with its dimension items

        :param dimensionId: dimension identifier, integer
        :return: dimension with its dimension items, dict
        """

        method = "GET"
        endpoint = "dimensions/{}".format(str(dimensionId))

        return self.request(method, endpoint)

    # FISCAL YEARS
    def get_fiscal_years(self):
        """Gets and returns fiscal years ordered by their start date, from newest to oldest. Tracking periods, if exist, are in chronological order. Fiscal years can be edited on the Fiscal years page in Procountor.

        :return: list of fiscal years, dict
        """

        method = "GET"
        endpoint = "fiscalyears"

        return self.request(method, endpoint)

    # LEDGER RECEIPTS
    def get_ledger_receipts(self, previousId, **kwargs):
        """Method gets and returns a list containing basic information for the receipts. The receiptID in each result entry can be used to fetch complete receipt details with the GET /ledgerereceipts/{receiptId} endpoint, get_ledger_receipt() method. Supported ledger receipt types are journals, sales invoice ledger receipts and purchase ledger invoice receipts.

        :param previousId: previous ledger receipt ID for pagination, string
        :param startDate: start date of the search (yyyy-MM-dd), string
        :param endDate: end date of the search (yyyy-MM-dd), string
        :param types: ledger receipt types, list of strings, possible values: 'JOURNAL', 'PURCHASE_INVOICE', 'SALES_INVOICE', 'PERIODIC_TAX_RETURN'
        :param orderById: order the results by ledger receipt ID ('asc' or 'desc'), string
        :return: list containing basic information for the receipts, dict
        """

        method = "GET"
        endpoint = "ledgerreceipts"

        if kwargs is not None:
            endpoint += "?"
            index = 0
            for key, value in kwargs.items():
                index += 1
                if index < len(kwargs):
                    endpoint += "{}={}&".format(key, str(value))
                else:
                    endpoint += "{}={}&previousId={}".format(key, str(value), str(previousId))
        else:
            raise ValueError("No data given")

        return self.request(method, endpoint)

    def get_ledger_receipt(self, receiptId):
        """Method gets and returns the requested ledger receipt. Supported ledger receipt types are journals, sales invoice ledger receipts and purchase invoice ledger receipts

        :param receiptId: ledger receipt identifier, integer
        :return: requested ledger receipt, dict
        """

        method = "GET"
        endpoint = "ledgerreceipts/{}".format(str(receiptId))

        return self.request(method, endpoint)

    def post_ledger_receipt(self, **kwargs):
        """Method sends new ledger receipt to Procountor, Supports journal type ledger receipts

        :param kwargs: ledger receipt data, dict
        """

        method = "POST"
        endpoint = "ledgerreceipts"

        if kwargs is None:
            raise ValueError('No data given')

        return self.request(method, endpoint, **kwargs)

    def update_ledger_receipt(self, receiptId, **kwargs):
        """Method updates requested ledger receipt in Procountor environment. Supported ledger receipt types are journals, sales invoice ledger receipts and purchase invoice ledger receipts. For defining the ledger accounts, dimensions, VAT status or other accounting information for an invoice, use this method.

        :param receiptId: ledger receipt identifier, integer
        :param kwargs: ledger receipt data, dict
        """

        method = "PUT"
        endpoint = "ledgerreceipts/{}".format(str(receiptId))

        if kwargs is None:
            raise ValueError('No data given')

        return self.request(method, endpoint, **kwargs)

    # CHART OF ACCOUNTS
    def get_coa(self):
        """Method gets and returns the chart of accounts for the current environment. It can be modified on the Chart of accounts page in Procountor.

        :return: chart of accounts for the current environment, dict
        """

        method = "GET"
        endpoint = "coa"

        return self.request(method, endpoint)

    # BUSINESS PARTNERS
    def get_business_partner(self, partnerId):
        """Method gets and returns requested business partner with its address

        :param partnerId: business partner's identifier, integer
        :return: information of business partner with its address, dict
        """

        method = "GET"
        endpoint = "businesspartners/{}".format(str(partnerId))

        return self.request(method, endpoint)

    # BANK STATEMENTS
    def get_bank_statements(self, startDate, endDate):
        """Gets and returns all bank statements that match the request criteria. Each BankStatementEvent can have a list of child events. In that case, the event model contains an additional "event" property with an array of BankStatementEvents as its value.

        :param startDate: Start date of the search (yyyy-MM-dd), string
        :param endDate: End date of the search (yyyy-MM-dd), string
        :return: all bank statements that match the request criteria, dict
        """

        method = "GET"
        endpoint = "bankstatements?startDate={}&endDate={}".format(startDate, endDate)

        return self.request(method, endpoint)

    def delete_products_from_bank_statement(self, statementId, eventId):
        """Method deletes allocation of a product from a bank statement event

        :param statementId: ID of the bankstatement, integer
        :param eventId: ID of the event, integer
        """

        method = "DELETE"
        endpoint = "bankstatements/{}/events/{}/products".format(str(statementId), str(eventId))

        return self.request(method, endpoint)

    def put_products_to_bank_statement(self, statementId, eventId, **kwargs):
        """Method allocates a product to a bank statement event

        :param statementId: ID of the bankstatement, integer
        :param eventId: ID of the event, integer
        :param body: product information, dict
        """

        method = "PUT"
        endpoint = "bankstatements/{}/events/{}/products".format(str(statementId), str(eventId))

        return self.request(method, endpoint, **kwargs)
        
    # ATTACHMENTS
    def get_attachment(self, attachmentId):
        """Gets and returns an attachment based on given attachment ID. Both attachment metadata (application/json) and the file itself will be returned. Content-type for the response is multipart/mixed.

        :param attachmentId: ID of the requested attachment, integer
        :return: attachment metadata (dict) and file itself
        """
        method = "GET"
        endpoint = "attachments/{}".format(str(attachmentId))

        return self.request(method, endpoint)

    def delete_attachment(self, attachmentId):
        """Deletes requested attachment

        :param attachmentId: ID of the requested attachment to delete, integer
        """
        method = "DELETE"
        endpoint = "attachments/{}".format(str(attachmentId))

        return self.request(method, endpoint)

    def post_attachment(self, meta, filename):
        """Method sends new attachment to Procountor. The attachment can be of any type but limited to max 10000000 bytes (10MB). Content-type for the request is multipart/form-data. Type for the meta data is application/json.

        :param meta: meta data for attachment, contains name of the file, referenceType and referenceId of the attachment, dict
        :param filename: path to the file
        """
        method = "POST"
        endpoint = "attachments"

        with open(filename, "rb") as f:
            files = {
                'meta': (None, json.dumps(meta), "application/json"),
                'file': f.read(),
            }

            r = requests.request(method, self.api_url + endpoint, files=files, headers=self.headers(method, endpoint))
            if r.status_code == 401:
                self.access_token = self.refresh_access_token(self.refresh_token)
                r = requests.request(method, self.api_url + endpoint, files=files, headers=self.headers(method, endpoint))
                return r.text
            else:
                return r.text

    def request(self, method, endpoint, *args, **kwargs):
        """Method to make HTTP requests over Procountor REST API

        :param method: wanted request method, uppercase string
        :param endpoint: wanted REST API endpoint, string
        :param kwargs: query parameters to pass to Procountor, dict
        :return: response from rest server, dict
        """

        r = requests.request(method, self.api_url + endpoint, headers=self.headers(method, endpoint), json=kwargs)
        if r.status_code == 401:
            self.access_token = self.refresh_access_token(self.refresh_token)
            r = requests.request(method, self.api_url + endpoint, headers=self.headers(method, endpoint), json=kwargs)
            r.raise_for_status()
            return r.text
        else:
            return r.text

    def headers(self, method, endpoint):
        """Method returns correct headers for request.

        :param method: request method, string
        :param endpoint: request endpoint, string
        :return: headers for request, dict
        """

        if "attachments" in endpoint:
            if method == "GET":
                headers = {
                    'content-type': 'multipart/mixed',
                    'authorization': 'Bearer {}'.format(self.access_token),
                }
            elif method == "POST":
                headers = {
                    # can't put 'content-type': 'multipart/form-data' here as documentation says. Requests generates it automatically.
                    'authorization': 'Bearer {}'.format(self.access_token),
                }
            else:
                headers = {
                    'content-type': 'application/json',
                    'authorization': 'Bearer {}'.format(self.access_token),
                }
        else:
            headers = {
                'content-type': 'application/json',
                'authorization': 'Bearer {}'.format(self.access_token),
            }

        return headers