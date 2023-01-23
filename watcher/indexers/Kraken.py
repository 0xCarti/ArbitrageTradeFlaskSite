import requests

class Kraken:
    def __init__(self):
        self.base_path = 'https://api.kraken.com/0'


    def get_price(self, ticker: str):
        ticker = f'X{ticker[:3]}Z{ticker[3:]}'
        if 'BTC' in ticker:
            ticker = ticker.replace("BTC", "XBT")
        response = requests.get(f'{self.base_path}/public/Ticker?pair={ticker}')
        return float(response.json()['result'][ticker]['c'][0])

    def get_fees(self, ticker: str = ''):
        return 0.2

if __name__ == "__main__":
    client = Kraken()
    print(client.get_price('BTCUSD'))