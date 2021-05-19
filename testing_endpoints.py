from ClientEtherScan import ClientEtherScan
import json

API_KEY = 'AIZ32QT1EWEKQN27W2IGY2VVGWP317MBEZ'

client = ClientEtherScan(API_KEY = API_KEY)

address = '0xa478c2975ab1ea89e8196811f51a7b7ade33eb11'
startblock = 12461658
endblock = 12461658
transactions = client.get_list_of_ERC20_toker_transfer_by_adress(address = address, startblock = startblock, endblock = endblock)['result']

all_transactions = dict()

for tsf1 in transactions:
    for tsf2 in transactions:
        if ((tsf1 != tsf2) and (tsf1['hash'] == tsf2['hash'])):

            hash =tsf1['hash']

            if hash not in all_transactions.keys():
                all_transactions[hash] = []

            if tsf1 not in all_transactions[hash]:
                all_transactions[hash].append(tsf1)

            if tsf2 not in all_transactions[hash]:
                all_transactions[hash].append(tsf2)



# print(all_transactions)
print(json.dumps(all_transactions, indent = 2))


# print(json.dumps(transactions, indent = 2))
