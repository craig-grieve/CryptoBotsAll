# -*- coding: utf-8 -*-
import os, sys
# https://codeolives.com/2020/01/10/python-reference-module-in-parent-directory/
currentdir = os.path.dirname(os.path.realpath(__file__))
parentdir = os.path.dirname(currentdir)
sys.path.append(currentdir)
#print(sys.version)

import json
import requests
import time
import base64
import hmac
import hashlib
import pandas as pd
import numpy as np
import time
import config


"""
TODO: Total sum of single ACCOUNT
TODO: Total sum of all ACCOUNTS
TODO: GET all orders for a single coin
TODO: POST order for a single coin
TODO: DELETE an order
TODO: GET Order Book

TODO: TESTS!!!!!!! TESTS!!!!! TESTS!!!!!!!

"""

class KuCoin:
    """

    """
    SANDBOX = False
    LIVE = False
    DEBUG = True
    TRADABLE_COINS = []
    TRADABLE_ACCOUNTS = ['main', 'trade']
    ACCOUNTS = pd.DataFrame()
    ALLOWED_ACCOUNTS = pd.DataFrame()


    def __init__(self, debug=True, sandbox=False):
        # Check in with Kucoin and make sure there is a valid response
        self.DEBUG = debug
        self.SANDBOX = sandbox

        if self.DEBUG:
            print('----', 'Init', '----')
            print('DEBUG:', self.DEBUG)
            print('SANDBOX:', self.SANDBOX)
            print('IP:', self.__get_ip())
            print('PYTHON VERSION:',sys.version)
            print('')

        self.__update_account_balances()
        #self.__get_all_account_tickers()
        #self.get_all_market_tickers()


    def __get_ip(self):
        ip = requests.get('https://api.ipify.org').text
        return ip


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

    def __send_request(self, endpoint, data={}):
        """
        Returns the response from the API after forming the request

        endpoint: string endpoint of the API including any GET variables
        """

        url = self.__configure_URL(endpoint)

        if not data:
            if self.DEBUG:
                print('Sending GET request:', url)

            headers = self.__create_headers(endpoint, 'GET', '')
            r = requests.request('get', url, headers=headers)
        else:
            if self.DEBUG:
                print('Sending POST request:', url, data, '')

            headers = create_post_headers(endpoint, data=data)
            jsn = json.dumps(data)
            r = requests.request('post', url, data=jsn, headers=headers)

        json_data = r.json()
        resp = self.__handle_return(json_data)

        return resp


    def __handle_return(self, response):
        """
        Returns the response of the API or the formated error response

        response:  the response from the API in a panda DataFrame
        """

        if response['code'] == '200000':
            ret_resp = pd.DataFrame(response['data'])

            if self.DEBUG:
                print("SUCCESSFUL Response")
                print(response['code'], ':', 'returned', len(response['data']), 'items of type ', type(response['data']) ,'::', ret_resp.columns)
                print('DataFrame:', ret_resp.shape)
                print('')

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
            if self.DEBUG:
                print('\n', 'There was an Error in the response', '\n')
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


    def __get_ticker(self, coin_pair):
        """
        """
        endpoint = '/api/v1/market/orderbook/level1?symbol=' + coin_pair
        resp = self.__send_request(endpoint)
        resp.columns = ['sequence', 'bestAsk', 'size', 'price', 'bestBidSize', 'bestBid', 'bestAskSize', 'time']


    def get_all_market_tickers(self):
        """
        Returns all the market tickers on KuCoin
        """

        endpoint = '/api/v1/market/allTickers'
        resp = self.__send_request(endpoint)

        tickers = resp['ticker']

        data = pd.json_normalize(tickers)

        cols = ['last', 'high', 'low', 'buy', 'sell', 'vol', 'volValue', 'averagePrice']
        data[cols] = data[cols].apply(pd.to_numeric, errors='coerce')

        return data


    def __add_markets_to_accounts(self):
        """
        Returns the account data combined with the market tickers
        """

        tickers = self.get_all_market_tickers()
        cols = ['balance']
        self.ACCOUNTS[cols] = self.ACCOUNTS[cols].apply(pd.to_numeric, errors='coerce')

        tickers['currency'] = tickers['symbol'].str.split('-').str[0]
        test = self.ACCOUNTS

        usdt = tickers[tickers['symbol'].str.contains('-USDT')]
        btc = tickers[tickers['symbol'].str.contains('-BTC')]

        test = pd.merge(test, usdt[['currency', 'last']], on='currency', how='left')
        test.rename(columns={'last': 'usdt'}, inplace=True)

        test = pd.merge(test, btc[['currency', 'last']], on='currency', how='left')
        test.rename(columns={'last': 'btc'}, inplace=True)

        test['btcDollar'] = test['btc'] * tickers.loc[tickers['symbol'] == 'BTC-USDT', 'last'].iloc[0]
        test['dollarValue'] = test.apply(self.__output_coin_type_value, axis=1)

        print(test[['currency', 'type', 'balance', 'dollarValue']])
        print(test['dollarValue'].sum())



        if self.DEBUG:
            print('')
            print('ACCOUNTS:', self.ACCOUNTS.shape)


    def __output_coin_type_value(self, row):
        """
        Returns the value of the column to use to calculate the dollar value of the asset
        """
        if not np.isnan(row['usdt']):
            return row['usdt'] * row['balance']
        elif not np.isnan(row['btcDollar']):
            return row['btcDollar'] * row['balance']
        elif row['currency'] == 'USDT':
            return 1.00 * row['balance']


    def __update_account_balances(self):
        """
        Returns a list of all the accounts attached to the KuCoin Main accounts

        resp: The response
        """
        endpoint = "/api/v1/accounts"
        resp = self.__send_request(endpoint)

        if(self.__no_error_in_response(resp)):
            self.ACCOUNTS = resp
            cols = ['balance']
            self.ACCOUNTS[cols] = self.ACCOUNTS[cols].apply(pd.to_numeric, errors='coerce')

            self.__add_markets_to_accounts()


            if self.DEBUG:
                if self.ACCOUNTS.shape[0] > 0:
                    print("Connected {} accounts from KuCoin API".format(self.ACCOUNTS.shape[0]))
                    print('')
            return True
        else:
            return False


    def place_single_order(self, coin, quanity):
        """

        """

        # Check coin is Allowed
        # Check quanity is available
        return True


    def delete_single_order(self, order_id):
        """
        """

        # cancel the order
        return True


    def get_orders(self, coin):
        """
        """

        # Check coin is Allowed
        # Handle limting the orders
        return True


    def __check_candle_type(self, candle_type):
        """
        Returns the number of minutes if the candle type is in the allowed types

        candle_type: string of the candle type
        """

        allowed_types = {
            '1min': 1,
            '4hour': 240
        }

        if candle_type in allowed_types:
            return allowed_types[candle_type]
        else:
            return False


    def __calculate_chunk_times(self, i, chunk, candle_seconds, now):
        """
        returns the start and end times in seconds

        i: number of chunks
        chunk: the number of lookbacks
        candle_seconds: how many seconds per candle / lookback
        now: The time now in seconds for the hard end time
        """
        chunk_seconds = chunk * candle_seconds

        startedAt = int((now - chunk_seconds) - (i * chunk_seconds))
        endAt = int(now - (i * chunk_seconds))

        return startedAt, endAt

    def get_market_data(self, candle_type, coin_pair, lookback):
        """
        Returns the market data for a set coin

        TODO: This data should be stored in the class for retrieval later
        TODO: This should make a request for less data based on the data stored in the class, or csv
        """

        # The maximum the API will return is 1500
        # Set chunk limits
        chunk = 1000
        1000 if chunk >= lookback else lookback
        data = pd.DataFrame(columns=['time', 'open', 'close', 'high', 'low', 'volume', 'turnover'])


        candle_mins = self.__check_candle_type(candle_type)
        candle_seconds = candle_mins * 60
        now = time.time()

        times = int(lookback / chunk)

        # Set a rate limit of 10
        10 if times > 10 else times

        for i in range(times):
            endpoint = '/api/v1/market/candles'
            calc_chunk = chunk
            startedAt, endAt = self.__calculate_chunk_times(i, calc_chunk, candle_seconds, now)
            # This does not account for the remainder chunk: 1001 lookback will provide 2000 data

            variables = '?type={}&symbol={}&startAt={}&endAt={}'.format(
                candle_type, coin_pair, startedAt, endAt
            )

            # Get request
            endpoint = endpoint + variables
            resp = self.__send_request(endpoint)
            resp.columns = ['time', 'open', 'close', 'high', 'low', 'volume', 'turnover']

            if(self.__no_error_in_response(resp)):
                data = data.append(resp)


        if self.DEBUG:
            print('times to run:', times, 'dataframe:', data.shape)

        data = self.__convert_time(data)

        return data


    def __convert_time(self, df):
        """
        Returns the dataframe with the time converted into a datetime

        df: DataFrame
        """

        df['time'] = pd.to_datetime(df['time'], unit='s')

        return df


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



kk = KuCoin()
print(kk.ACCOUNTS)
