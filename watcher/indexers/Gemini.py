from decimal import Decimal

from gemini_api.endpoints.public import Public
from gemini_api.authentication import Authentication


class Gemini:
    def __init__(self, public_key: str = None, private_key: str = None):
        if public_key is not None and private_key is not None:
            self.PUBLIC_KEY = public_key
            self.PRIVATE_KEY = private_key
            self.auth = Authentication(public_key=self.PUBLIC_KEY, private_key=self.PRIVATE_KEY, sandbox=True)
        self.public = Public(sandbox=True)

    def get_price(self, ticker: str):
        return Decimal(self.public.get_ticker_prices(ticker)['close'])

    def get_pairs(self):
        return self.public.get_pairs()