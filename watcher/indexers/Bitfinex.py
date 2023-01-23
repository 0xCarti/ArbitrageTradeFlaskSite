import requests


class Bitfinex:
    def __init__(self):
        self.base_path = 'https://api-pub.bitfinex.com'
        self.headers = {"accept": "application/json"}

    def get_price(self, ticker: str):
        url = "https://api-pub.bitfinex.com/v2/ticker/tBTCUSD"
        response = requests.get(f'{self.base_path}/v2/ticker/t{ticker}', headers=self.headers)
        return float(response.json()[6])

    def get_fees(self, ticker: str = ''):
        return 0.2

if __name__ == "__main__":
    client = Bitfinex()
    print(client.get_price('BTCUSD'))