import requests


class CurrencyConverter:
    def convert(self, buy_curr: str, sell_curr: str, price: float):
        url = f'https://api.exchangerate.host/convert?from={sell_curr}&to={buy_curr}&amount={price}&places=2'
        try:
            response = requests.get(url)
        except ConnectionError:
            print(f'Connection Error Trying Again.')
            response = requests.get(url)
        data = response.json()
        return float(data['result'])


if __name__ == '__main__':
    indexer = CurrencyConverter()
    print(indexer.convert('USD', 'CAD', 1000.25))
