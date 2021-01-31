import json
import requests
import time
import base64
import hmac
import hashlib


class KuCoin:

    def __init__(self):
        # Check in with Kucoin and make sure there is a valid response
        pass

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


    def get_account_balances():
        pass









    def delete_active_loan(id):
        """
        Deletes a specif loan order

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
