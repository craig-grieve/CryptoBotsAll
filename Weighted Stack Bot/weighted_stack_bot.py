import os, sys
# https://codeolives.com/2020/01/10/python-reference-module-in-parent-directory/
currentdir = os.path.dirname(os.path.realpath(__file__))
parentdir = os.path.dirname(currentdir)
sys.path.append(parentdir)
from KuCoin import kucoin
from ChartAnalyzer import chartAnalyzer


class WeightedStackBot:
    """
    This bot will place orders on a coin with weightings to the extremes.
    Buy more low and sell more high.

    """
    ANALYZER = chartAnalyzer.ChartAnalyzer()
    API = ''
    HARDCODED_COINS = [
        'BTC', 'ETH', 'XPR', 'KCS', 'DOT', 'MTV', 'TRX',
        'REVV', 'ZIL', 'VET', 'RFUEL', 'LTC', 'LINK'
        ]
    ACTIVE = False
    DEBUG = True
    SANDBOX = False
    FUNDS = 0
    TARGET_COIN = 'BTC'
    ACTIVE_ORDERS = []
    CLOSED_ORDERS = []
    """
    Order: {
        'status': 'Active' or 'Closed'
        'buy_id': string,
        'buy_price': number,
        'sell_id': string,
        'sell_price': number,
        'coin_profit': number,
        'dollar_profit': number
    }
    """

    def __init__(self):
        self.__connect_to_kucoin_api()
        self.API.get_market_data('1min', 'BTC-USDT', 10)


    def __connect_to_kucoin_api(self):
        """
        Connects to the KuCoin Api
        """
        self.API = kucoin.KuCoin(debug=self.DEBUG, sandbox=self.SANDBOX)
        return True


    def __set_target_coin(self, coin):
        """
        Sets the Bots target coin to track
        """
        if coin in self.HARDCODED_COINS:
            self.TARGET_COIN = coin

            if self.DEBUG:
                print('Target Coin set to:', self.TARGET_COIN, '\n')
            return True
        else:
            return False


    def __set_funds(self, funds):
        """
        """

        if type(funds) is int:
            # Get funds from Kucoin
            # Check funds is less than this value
            self.FUNDS = funds
        else:
            print('Funds were not an INT.', 'Did not set any funds', '\n')


    # Get limits and settings
    def update_settings(self, settings={}):
        """
        This is a handler for any settings that need to be changed for the BOT.

        settings: an object full of any settings:
            coin: string of coin ticker
            funds: int of funds you want to use
        """
        if 'coin' in settings:
            self.__set_target_coin(settings['coin'])
        if 'funds' in settings:
            # Should checks funds exist and is an int
            self.__set_funds(settings['funds'])


    # Gather 4 hour tick data for coin

    # Get minute tick data for coin
    def get_minute_tick_data(self, lookback):
        data = self.API.get_market_data('1min', self.TARGET_COIN+'-USDT', 1000)
        print(data.head())

    # Save tick data to file

    # Load tick data

    # Buy in with some initial capital

    # Calculate Spread of orders
    # Calculate minimums
    # Calculate maximums
    # Calculate weights

    # Ensure order will be profit

    # Place the orders

    # Cash out

    # Count value in active orders

    # Count value in closed orders


wsb = WeightedStackBot()
wsb.update_settings(settings = {'funds': 100})

wsb.get_minute_tick_data(1000)

print(wsb.FUNDS)








#

#

# Get current price

# Calculate the best stack

# Peak shift over last day

# Cut under/over

# Weight the stack

# Check not selling at a loss

    # Each completed buy order needs a corresponding sale order

    # If not previous recent data above position then at increments6

# re-place orders

#

#
