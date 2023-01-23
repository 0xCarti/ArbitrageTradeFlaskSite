import requests


class CEXIO:
    def __init__(self):
        self.headers = {'Accept': '*/*'}

    def get_price(self, ticker: str):
        r = requests.get(f'https://cex.io/api/last_price/{ticker[:3]}/{ticker[3:]}', headers=self.headers)
        return float(r.json()['lprice'])

    def get_fees(self, ticker: str = ''):
        return 0.25

if __name__ == "__main__":
    client = CEXIO()
    print(client.get_price('BTCUSD'))
