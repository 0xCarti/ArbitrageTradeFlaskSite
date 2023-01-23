import json
from datetime import datetime
import threading
import time

from objects.IndexerManager import IndexerManager
from objects.MarketManager import MarketManager
from objects.Settings import Settings
from objects.ThreadManager import ThreadManager
from objects.TradeManager import TradeException, TradeManager

pairs = []
trades = []
indexers = IndexerManager()
settings = Settings()
markets = MarketManager()
markets.enable_markets('BTCUSD', 'BTCEUR', 'BTCCAD')
#settings.set('price_thresh', 10.0)
settings.set('price_thresh', 0.0)
settings.set('interval', 1800)
threads = ThreadManager(settings)
trader = TradeManager(indexers, settings, threads)

for buy_market in markets:
    for sell_market in markets:
        for buy_exchange in markets.get(buy_market):
            for sell_exchange in markets.get(sell_market):
                try:
                    trade = trader.create_trade(buy_exchange, buy_market, sell_exchange, sell_market)
                except TradeException as e:
                    pass


print(f'Loaded {len(trader.trades)} trades into the trader.')
while True:
    timestamp = datetime.now().strftime("%m/%d/%Y, %H:%M:%S")
    print(f'{timestamp}'.center(70, '-'))
    for index in range(1, settings.get('thread_limit')):
        name = f'Thread-{index}'
        thread = threading.Thread(target=trader.monitor, args=(timestamp, (index * 5) - 5, index * 5, name), name=name)
        threads.add_thread(thread)
    while not threads.is_all_stopped():
        pass
    print(''.center(70, '-'))
    threads.clear()
    interval = settings.get('interval')
    time.sleep(interval)
