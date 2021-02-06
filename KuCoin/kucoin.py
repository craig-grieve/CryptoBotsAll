# -*- coding: utf-8 -*-
import os, sys
# https://codeolives.com/2020/01/10/python-reference-module-in-parent-directory/
currentdir = os.path.dirname(os.path.realpath(__file__))
parentdir = os.path.dirname(currentdir)
sys.path.append(currentdir)

import json
import requests
import time
import base64
import hmac
import hashlib
import pandas as pd
import config

"""
TODO: Account Breakouts
TODO: Allowed Account Breakouts
TODO: Total sum of single ACCOUNT
TODO: Total sum of all ACCOUNTS
TODO: GET all orders for a single coin
TODO: POST order for a single coin
TODO: DELETE an order
TODO: GET Market Tickers
TODO: GET Order Book

"""

class KuCoin:
    """

    """
    SANDBOX = False
    LIVE = False
    DEBUG = False
    TRADABLE_COINS = []
    TRADABLE_ACCOUNTS = ['main', 'trade']
    ACCOUNTS = pd.DataFrame()
    ALLOWED_ACCOUNTS = pd.DataFrame()


    def __init__(self, debug=False):
        # Check in with Kucoin and make sure there is a valid response
        self.DEBUG = debug

        if self.DEBUG:
            print('----', 'Init', '----')
            print('DEBUG:', self.DEBUG)
            print('SANDBOX:', self.SANDBOX)
            print('')
        self.__update_account_balances()




    def __create_headers(self, endpoint, header_type='GET', data={}):
        """
        returns the headers for the API

        endpoint: the API endpoint to go to
        header_type: GET, POST, DELETE
        data: JSON object to send
        """
        now = int(time.time() * 1000)

        if header_type == 'GET' or header_type == 'DELETE':
            str_to_sign = str(now) + str(header_type) + endpoint
        elif header_type == 'POST':
            str_to_sign = str(now) + 'POST' + str(endpoint) + str(json.dumps(data))
        else:
            # Fail in some way
            print('Error: Could not set headers')
            return False

        signature = base64.b64encode(
            hmac.new(config.API_SECRET.encode('utf-8'),
            str_to_sign.encode('utf-8'),
            hashlib.sha256).digest())

        passphrase = base64.b64encode(
            hmac.new(config.API_SECRET.encode('utf-8'),
            config.API_PASSPHRASE.encode('utf-8'),
            hashlib.sha256).digest())

        headers = {
            'KC-API-SIGN': signature,
            'KC-API-TIMESTAMP': str(now),
            'KC-API-KEY': config.API_KEY,
            'KC-API-PASSPHRASE': passphrase,
            'KC-API-KEY-VERSION': str(2),
            }

        if header_type == 'POST':
            headers['Content-Type'] = 'application/json'

        return headers


    def __handle_return(self, response):
        """
        Returns the response of the API or the formated error response

        response:  the response from the API in a panda DataFrame
        """

        if response['code'] == '200000':
            if self.DEBUG:
                print("SUCCESSFUL Response")
                print(response['code'], ':', response['data'])
                print('')

            ret_resp = pd.DataFrame(response['data'])
            return ret_resp
        else:
            # Handle the individual responses here
            if self.DEBUG:
                print("FAILED Response")
                print(response['code'], ':', response['msg'])
                print('')
            return 'Error: ' + response['msg']


    def __no_error_in_response(self, response):
        """
        Returns true if the repsonse does not contain and error and False if it does
        """
        if isinstance(response, pd.DataFrame):
            return True
        else:
            if response[:6] == "Error:":
                return False
            else:
                return True


    def __configure_URL(self, endpoint):
        """
        Retruns the url depending on the mode of the KuCoin class

        endpoint: the API address
        data: any json data payload
        """

        if self.SANDBOX == True:
            url = config.SANDBOX_API_URL + endpoint
        else:
            url = config.API_URL + endpoint

        return url


    def set_tradable_coins(self, coins=[]):
        """
        Sets the coins that we are allowed to trade

        coins: an array of coin tickers
        """
        # Should check the coins entered are valid
        # Should make sure there are funds available
        self.TRADABLE_COINS = []
        return True


    def tradable_coins(self):
        """
        Future proofing, might want to make further checks here at some point
        """
        if is_empty(self.TRADABLE_COINS):
            return False
        else:
            return True


    def __update_account_balances(self):
        """
        Returns a list of all the accounts attached to the KuCoin Main accounts

        resp: The response
        """
        endpoint = "/api/v1/accounts"
        url = self.__configure_URL(endpoint)
        headers = self.__create_headers(endpoint, 'GET')
        r = requests.request('get', url, headers=headers)

        json_data = r.json()
        resp = self.__handle_return(json_data)

        if(self.__no_error_in_response(resp)):
            self.ACCOUNTS = resp

            # Breakout ACCOUNTS
            # Breakout Allowed ACCOUNTS

            #resp = resp.loc[resp['type'] == 'main']

            if self.DEBUG:
                if self.ACCOUNTS.shape[0] > 0:
                    print("Connected {} accounts from KuCoin API".format(self.ACCOUNTS.shape[0]))
                    print('')
            return True
        else:
            return False


    def delete_active_loan(self, id):
        """
        Deletes a specific loan order

        id: a String of the loan order id

        return: Boolean
        """
        return True


    def get_active_loans(self, coins=[]):
        """
        Retruns the list of active loans for the coins

        coins: a list of coins to return

        response: an object of the responses
        """
        response = {}

        for i in range(len(coins)):
            response[coins['i']] = __get_active_loans_single_coin(coins['i'])

        return response


    def __get_active_loans_single_coin(self, coin='BTC'):
        """
        Returns the list of active loan orders for a single coins

        coin: a String of the single coin
        """
        return False
