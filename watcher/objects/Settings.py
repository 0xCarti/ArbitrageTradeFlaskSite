class Settings:
    def __init__(self, settings: dict = None):
        if settings is None:
            settings = {'interval': 300, 'price_thresh': 0.0, 'thread_limit': 8}
        self.settings = settings
        self.lock = False

    def set(self, setting: str, value):
        self.settings[setting] = value

    def get(self, setting: str):
        return self.settings[setting]