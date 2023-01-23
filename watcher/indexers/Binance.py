import requests


class Binance:
    def __init__(self):
        self.headers = {'GET': '*/*'}
        self.base_path = 'https://data.binance.com/api'

    def get_price(self, ticker: str):
        if 'USD' in ticker:
            ticker = ticker.replace('USD', 'USDT')
        r = requests.get(f'{self.base_path}/v3/ticker/price?symbol={ticker}', headers=self.headers)
        return float(r.json()['price'])

    def get_fees(self, ticker: str = ''):
        return 0


if __name__ == '__main__':
    indexer = Binance()
    print(indexer.get_price('BTCUSD'))
