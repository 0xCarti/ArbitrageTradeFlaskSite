class MarketManager:
    def __init__(self):
        self.enabled_markets = {}
        self.all_markets = {
            'BTCUSD': [
                'binance',
                'kraken',
                # 'gemini',
                'cexio',
                'bitfinex',
            ],
            'BTCEUR': [
                'binance',
                'kraken',
                # 'gemini',
                'cexio',
                'bitfinex',
            ],
            'BTCCAD': [
                'kraken',
            ]}

    def enable_markets(self, *markets: str):
        for market in markets:
            if market in self.all_markets:
                self.enabled_markets[market] = self.all_markets[market]

    def disable_markets(self, *markets: str):
        for market in markets:
            if market in self.enabled_markets:
                self.enabled_markets.pop(market)

    def get(self, market: str):
        if market in self.enabled_markets:
            return self.enabled_markets[market]
        else:
            return self.all_markets[market]

    def __iter__(self):
        return self.enabled_markets.__iter__()