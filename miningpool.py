import requests

class MiningPool:
    def __init__(self, name : str, url : str, balance_field : str, hashrate_field : str):
        self.name = name
        self.url = url
        self.balance_field = balance_field
        self.hashrate_field = hashrate_field

    def getminingdata(self, wallet_address):
        # Ravenminer and 2miners have an open api and don't require registration
        headers = {
            'accept': 'application/json',
        }

        print(requests.get(self.url + wallet_address, headers=headers).content)



