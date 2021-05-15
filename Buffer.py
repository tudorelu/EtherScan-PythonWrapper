import sys
sys.path.append('..')

import json
import time

from ClientEtherScan import ClientEtherScan

API_KEY = 'AIZ32QT1EWEKQN27W2IGY2VVGWP317MBEZ'

def main():
    client = ClientEtherScan(API_KEY = API_KEY)
    interval = 1

    # Some random address or list of addressess
    address = '0xee17a472aec51a95882475fd455d15c9e0d4db89'

    # now = int(time.time())
    now = int(time.time()) - 3600
    past_block = client.get_block_number_by_timestamp(timestamp = now, closest_value = 'before')['result']

    transactions = client.get_list_of_transactions(address = address, startblock = past_block, endblock = 99999999)

    while True:
        try:
            now = int(time.time())
            current_block = client.get_block_number_by_timestamp(timestamp = now, closest_value = 'before')['result']

            '''
            if we use a list of addressess simply use a for loop to iterate through each address

            for address in addresses:
                transactions = client.get_list_of_transactions(address = address, startblock = past_block, endblock = 99999999)

                for trans in transactions:
                    print(json.dumps(trans, indent = 2))
            '''

            transactions = client.get_list_of_transactions(address = address, startblock = past_block, endblock = current_block)
            for trans in transactions['result']:
                print(json.dumps(trans, indent = 2))

            past_block = current_block
            time.sleep(interval)
        except Exception as e:
            print(e)

if __name__ == '__main__':
    main()
