import requests

class ClientEtherScan:
    def __init__(self, API_KEY):
        self.base = 'https://api.etherscan.io/api?module='
        self.API_KEY = API_KEY

    def request_get(self, endpoint, params = {}):
        return requests.get(self.base + endpoint, params).json()

    def get_block_number_by_timestamp(self, timestamp = int(), closest_value = str()):
        '''
        [Parameters] timestamp format: Unix timestamp
         (supports Unix timestamps in seconds), closest value: 'before' or 'after'
        '''
        return self.request_get('block&action=getblocknobytime&timestamp='+str(timestamp)+'&closest='+closest_value+'&apikey='+self.API_KEY)

    def get_list_of_transactions(self, address = str(), startblock = int(), endblock = int()):
        return self.request_get('account&action=txlist&address='+str(address)+'&startblock='+str(startblock)+'&endblock='+str(endblock)+'&sort=asc&apikey='+self.API_KEY)
