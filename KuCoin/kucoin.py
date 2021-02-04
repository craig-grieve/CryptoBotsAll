import json
import requests
import time
import base64
import hmac
import hashlib


class KuCoin(DEBUG=True):
    """

    """

    TRADABLE_COINS = []


    def __init__(self):
        # Check in with Kucoin and make sure there is a valid response


        if DEBUG:
            print("Connected to KuCoin API")


    def __create_headers(endpoint, header_type='GET', data={}):
        """
        returns the headers for the API

        endpoint: the API endpoint to go to
        header_type: GET, POST, DELETE
        data: JSON object to send
        """
        now = int(time.time() * 1000)

        if header_type == 'GET' || header_type == 'DELETE':
            str_to_sign = str(now) + str(header_type) + endpoint
        else if header_type == 'POST':
            str_to_sign = str(now) + 'POST' + str(endpoint) + str(json.dumps(data))
        else:
            # Fail in some way
            print('Error: Could not set headers')
            return False

        signature = base64.b64encode(
            hmac.new(API_SECRET.encode('utf-8'),
            str_to_sign.encode('utf-8'),
            hashlib.sha256).digest())

        passphrase = base64.b64encode(
            hmac.new(API_SECRET.encode('utf-8'),
            API_PASSPHRASE.encode('utf-8'),
            hashlib.sha256).digest())

        headers = {
            'KC-API-SIGN': signature,
            'KC-API-TIMESTAMP': str(now),
            'KC-API-KEY': API_KEY,
            'KC-API-PASSPHRASE': passphrase,
            'KC-API-KEY-VERSION': str(2),
            }

        if header_type == 'POST':
            headers['Content-Type'] = 'application/json'

        return headers


    def __handle_return(response):
        """
        Returns the response of the API or the formated error response

        response:  the response from the API
        """

        if response['code'] == '200000':
            return reponse
        else:
            # Handle the individual responses here
            return 'Error: ' + response['msg']


    def set_tradable_coins(coins=[]):
        """
        Sets the coins that we are allowed to trade

        coins: an array of coin tickers
        """
        # Should check the coins entered are valid
        # Should make sure there are funds available
        TRADABLE_COINS = []
        return True


    def tradable_coins():
        """
        Future proofing, might want to make further checks here at some point
        """
        if is_empty(TRADABLE_COINS):
            return False
        else:
            return True


    def update_account_balances():
        """
        Returns a list of all the accounts attached to the KuCoin Main accounts

        resp: The response
        """
        endpoint = "/api/v1/accounts"
        url = API_URL + endpoint
        headers = create_get_headers(endpoint)
        r = requests.request('get', url, headers=headers)

        json_data = r.json()

        resp = pd.DataFrame(handle_return(json_data)['data'])
        resp = resp.loc[resp['type'] == 'main']

        if DEBUG:
        print_debug([resp])

        return resp



    def delete_active_loan(id):
        """
        Deletes a specific loan order

        id: a String of the loan order id

        return: Boolean
        """
        return True


    def get_active_loans(coins=[]):
        """
        Retruns the list of active loans for the coins

        coins: a list of coins to return

        response: an object of the responses
        """
        response = {}

        for i in range(len(coins)):
            response[coins['i']] = __get_active_loans_single_coin(coins['i'])

        return response


    def __get_active_loans_single_coin(coin='BTC'):
        """
        Returns the list of active loan orders for a single coins

        coin: a String of the single coin
        """
        return False
