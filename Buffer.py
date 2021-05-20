import sys
sys.path.append('..')

import json
import time
from datetime import datetime

from ClientEtherScan import ClientEtherScan
from discord import Webhook, RequestsWebhookAdapter
from web3 import Web3
import os

# from dotenv import load_dotenv
# load_dotenv()
# infura_project_id = os.getenv('INFURA_PROJECT_ID')
# w3 = Web3(Web3.HTTPProvider('https://mainnet.infura.io/v3/{}'.format(infura_project_id)))

API_KEY = 'AIZ32QT1EWEKQN27W2IGY2VVGWP317MBEZ'
client = ClientEtherScan(API_KEY = API_KEY)

def get_swaps(client, account, startblock, endblock):
    address = account['address']
    transactions = client.get_list_of_ERC20_toker_transfer_by_adress(address = address, startblock = startblock, endblock = endblock)['result']
    all_transactions = dict()
    for tsf1 in transactions:
        for tsf2 in transactions:
            if ((tsf1 != tsf2) and (tsf1['hash'] == tsf2['hash'])):
                hash = tsf1['hash']
                if hash not in all_transactions.keys():
                    all_transactions[hash] = []
                if tsf1 not in all_transactions[hash]:
                    all_transactions[hash].append(tsf1)
                if tsf2 not in all_transactions[hash]:
                    all_transactions[hash].append(tsf2)
    messages = []
    for hash in all_transactions.keys():
        from_tsf = None
        to_tsf = None
        for tsf in all_transactions[hash]:
            if address == tsf["from"]:
                from_tsf = tsf
            if address == tsf["to"]:
                to_tsf = tsf

        if from_tsf != None and to_tsf != None:
            # print(from_tsf)
            msg = ':star2: {} swapped {} {} for {} {} \n {}'.format(
                account['name'], 
                int(from_tsf['value']) / 10**int(from_tsf['tokenDecimal']), from_tsf['tokenSymbol'], 
                int(to_tsf['value']) / 10 **int(to_tsf['tokenDecimal']), to_tsf['tokenSymbol'],
                hash)

            messages.append(msg)

    return messages

def main():
    interval = 300

    # Some random address or list of addressess
    accounts = [
        dict(
            name='uniswap',
            address='0x1f9840a85d5af5bf1d1762f925bdaddc4201f984'),
        dict(
            name='Shroom Daddy',
            address='0xa9438f98df857b49afe08f467bc602a345c2995d'),
        dict(
            name='Austin Griffith',
            address='0x34aa3f359a9d614239015126635ce7732c18fdf3'),
        dict(
            name='Alex Becker',
            address='0xae4d837caa0c53579f8a156633355df5058b02f3'),
        dict(
            name='Mr. Beast',
            address='0x9e67d018488ad636b538e4158e9e7577f2ecac12')]

    # now = int(time.time())
    now = int(time.time()) - 600
    past_block = client.get_block_number_by_timestamp(timestamp = now, closest_value = 'before')['result']

    while True:
        # try:
            now = int(time.time())
            current_block = client.get_block_number_by_timestamp(timestamp = now, closest_value = 'before')['result']
            print('Current block is {}'.format(current_block))
            for account in accounts:
                address = account['address']
                result = client.get_list_of_transactions(address = address, startblock = past_block, endblock = 99999999)
                transactions = result['result']
                for trans in transactions:
                    msg = ''
                    if trans['from'] == address:
                        msg = ':detective: :eyes: New tx from {} at {}\n'.format(account['name'], datetime.fromtimestamp(int(trans['timeStamp'])))
                        msg += 'Sent {} ETH to {}\n'.format(Web3.fromWei(int(trans['value']), 'ether'), trans['to'])
                    else:
                        msg = ':detective: :eyes: New tx to {} at {}\n'.format(account['name'], datetime.fromtimestamp(int(trans['timeStamp'])))
                        msg += 'Received {} ETH from {}\n'.format(Web3.fromWei(int(trans['value']), 'ether'), trans['from'])

                    print(msg)
                    # discord_webhook.send(msg)

                messages = get_swaps(client = client, account = account, startblock = past_block, endblock = 99999999)
                for msg in messages:
                    print(msg)
                    discord_webhook.send(msg)
                    # print(json.dumps(transactions, indent = 2))

            # transactions = client.get_list_of_transactions(address = address, startblock = past_block, endblock = current_block)
            # for trans in transactions['result']:
            #     print(json.dumps(trans, indent = 2))

            past_block = current_block
            time.sleep(interval)
        # except Exception as e:
        #     print(e)


# address = '0xa478c2975ab1ea89e8196811f51a7b7ade33eb11'
# startblock = 12461650
# endblock = 12461658
# messages = get_swaps(client, dict(name='Lola', address=address), startblock, endblock)
# print(messages)

if __name__ == '__main__':
    discord_hook_url = 'https://discord.com/api/webhooks/842620311923982376/dQQsSiF-yt1bT9Urd3yYxQYvOyIjMIHEwKIN7Of8Vpl1eMzTYAko6D-C3FL6weGwAI3e'
    discord_webhook = Webhook.from_url(discord_hook_url, adapter=RequestsWebhookAdapter())
    # discord_webhook.send('testing hook')
    main()
