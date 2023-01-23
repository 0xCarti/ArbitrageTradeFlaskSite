from watcher.indexers.Binance import Binance
from watcher.indexers.Bitfinex import Bitfinex
from watcher.indexers.CEXIO import CEXIO
from watcher.indexers.Kraken import Kraken
#from indexers.Gemini import Gemini


class IndexerManager:
    def __init__(self):
        self.indexers = {
            'binance': Binance(),
            'kraken': Kraken(),
            #'gemini': Gemini(),
            'cexio': CEXIO(),
            'bitfinex': Bitfinex()
        }

    def get_indexer(self, name: str):
        return self.indexers[name]