from __future__ import annotations

from decimal import Decimal

from forex_python.converter import CurrencyRates

from watcher.objects.CurrencyConverter import CurrencyConverter
from watcher.objects.IndexerManager import IndexerManager
from watcher.objects.Settings import Settings
from watcher.objects.ThreadManager import ThreadManager
from watcher.objects.sql import SQLTrade, write_hero_to_database


class PairException(Exception):
    def __init__(self, message):
        super().__init__(message)


class TradeException(Exception):
    def __init__(self, message):
        super().__init__(message)


class Pair:
    def __init__(self, exchange: str, ticker: str, price: float = 0.0, fee_rate: float = 0.0):
        self.exchange = exchange
        self.ticker = ticker
        self.asset_one = ticker[:3]
        self.asset_two = ticker[3:]
        self.fee_rate = fee_rate

    def reverse(self):
        copy_asset = self.asset_one
        self.asset_one = self.asset_two
        self.asset_two = copy_asset

    def copy(self):
        return Pair(self.exchange, self.ticker)

    def __repr__(self):
        return f'{self.exchange} - {self.asset_one}/{self.asset_two}'


class Trade:
    def __init__(self, buy_pair: Pair, sell_pair: Pair):
        self.buy_pair = buy_pair
        self.sell_pair = sell_pair
        self.initial_currency = self.buy_pair.asset_two
        self.ending_currency = self.sell_pair.asset_two
        self.buy_fee = 0
        self.buy_price = 0
        self.sell_fee = 0
        self.sell_price = 0
        self.profit = 0.0

    def update_profit(self, indexer_manager: IndexerManager, rate_converter: CurrencyConverter):
        buy_indexer = indexer_manager.get_indexer(self.buy_pair.exchange)
        buy_curr = self.buy_pair.asset_two
        self.buy_price = buy_indexer.get_price(self.buy_pair.ticker)
        self.buy_fee = buy_indexer.get_price(self.buy_pair.ticker) * (self.buy_pair.fee_rate/100)
        sell_indexer = indexer_manager.get_indexer(self.sell_pair.exchange)
        sell_curr = self.sell_pair.asset_two
        self.sell_price = sell_indexer.get_price(self.sell_pair.ticker)
        self.sell_fee = sell_indexer.get_price(self.sell_pair.ticker) * (self.sell_pair.fee_rate/100)
        sell_price_converted = self.sell_price
        if buy_curr != sell_curr:
            sell_price_converted = rate_converter.convert(buy_curr, sell_curr, self.sell_price)
        self.profit = (sell_price_converted - self.buy_price) - (self.buy_fee + self.sell_fee)
        return self.profit

    def update_fee(self, ticker: str = ''):
        return

    def reverse(self):
        return Trade(self.sell_pair, self.buy_pair)

    def code(self) -> str:
        return f'{self.buy_pair.exchange}{self.buy_pair.ticker}{self.sell_pair.exchange}{self.sell_pair.ticker}'

    def __repr__(self):
        buy_trade = f'[{self.buy_pair.exchange}, {self.buy_pair.ticker}, {self.buy_price:.3f} + {self.buy_fee:.5f}]'.center(
            30, ' ')
        sell_trade = f'[{self.sell_pair.exchange}, {self.sell_pair.ticker}, {self.sell_price:.3f} + {self.sell_fee:.5f}]'.center(
            30, ' ')
        return f"{buy_trade} ---> {sell_trade}"


class TradeManager:
    def __init__(self, indexer_manager: IndexerManager, settings: Settings, threads: ThreadManager):
        self.indexer_manager = indexer_manager
        self.settings = settings
        self.threads = threads
        self.rate_converter = CurrencyConverter()
        self.trades = {}
        pass

    def create_trade(self, buy_exchange: str, buy_asset: str, sell_exchange: str, sell_asset: str):
        if buy_exchange == sell_exchange and buy_asset == sell_asset:
            raise TradeException(f'Trade Failed - Same Pair')
        buy_fee = self.indexer_manager.get_indexer(buy_exchange).get_fees(buy_asset)
        buy_pair = Pair(buy_exchange, buy_asset, fee_rate=buy_fee)
        sell_fee = self.indexer_manager.get_indexer(sell_exchange).get_fees(sell_asset)
        sell_pair = Pair(sell_exchange, sell_asset, fee_rate=sell_fee)
        if buy_pair.asset_one == sell_pair.asset_one:
            trade = Trade(buy_pair, sell_pair)
            reverse_code = trade.reverse().code()
            if reverse_code not in self.trades:
                self.trades[trade.code()] = trade
                return trade
        raise TradeException(f'Trade Failed - {buy_pair.asset_one}/{sell_pair.asset_one}')

    def monitor(self, time: str, start_index: int, end_index: int, thread_name: str, debug: bool = False):
        trade_codes = list(self.trades.keys())[start_index:end_index]
        for trade_code in trade_codes:
            trade, reverse_trade = self.trades[trade_code], self.trades[trade_code].reverse()
            profit = trade.update_profit(self.indexer_manager, self.rate_converter)
            if debug:
                print(f'{trade}\t[${profit:.6f} {trade.buy_pair.asset_two}]')
            reverse_profit = reverse_trade.update_profit(self.indexer_manager, self.rate_converter)
            if debug:
                print(f'{reverse_trade}\t[${reverse_profit:.6f} {reverse_trade.buy_pair.asset_two}]')
            if profit > self.settings.get('price_thresh') and not debug:
                while True:
                    if not self.settings.lock:
                        self.settings.lock = True
                        print(f'{trade}\t[${profit:.6f} {trade.buy_pair.asset_two}]')
                        sql_trade = SQLTrade(time=time,
                                             buy_exchange=trade.buy_pair.exchange,
                                             buy_market=trade.buy_pair.ticker,
                                             buy_price=trade.buy_price,
                                             buy_fee=trade.buy_fee,
                                             sell_exchange=trade.sell_pair.exchange,
                                             sell_market=trade.sell_pair.ticker,
                                             sell_price=trade.sell_price,
                                             sell_fee=trade.sell_fee,
                                             profit=profit)
                        write_hero_to_database(sql_trade)
                        self.settings.lock = False
                        break
            elif reverse_profit > self.settings.get('price_thresh') and not debug:
                while True:
                    if not self.settings.lock:
                        self.settings.lock = True
                        print(f'{reverse_trade}\t[${reverse_profit:.6f} {reverse_trade.buy_pair.asset_two}]')
                        sql_trade = SQLTrade(time=time,
                                             buy_exchange=reverse_trade.buy_pair.exchange,
                                             buy_market=reverse_trade.buy_pair.ticker,
                                             buy_price=reverse_trade.buy_price,
                                             buy_fee=reverse_trade.buy_fee,
                                             sell_exchange=reverse_trade.sell_pair.exchange,
                                             sell_market=reverse_trade.sell_pair.ticker,
                                             sell_price=reverse_trade.sell_price,
                                             sell_fee=reverse_trade.sell_fee,
                                             profit=reverse_profit)
                        write_hero_to_database(sql_trade)
                        self.settings.lock = False
                        break
        self.threads.stop_thread(thread_name)

    def reverse_trade(self):
        pass
