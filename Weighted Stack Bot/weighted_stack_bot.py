import os, sys
# https://codeolives.com/2020/01/10/python-reference-module-in-parent-directory/
currentdir = os.path.dirname(os.path.realpath(__file__))
parentdir = os.path.dirname(currentdir)
sys.path.append(parentdir)
from KuCoin import kucoin

# Load/Manage the active bot
kk = kucoin.KuCoin(debug=True)

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
