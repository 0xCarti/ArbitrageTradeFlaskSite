from threading import Thread

from objects.Settings import Settings


class ThreadManager:
    def __init__(self, settings: Settings):
        self.settings = settings
        self.running_threads = {}
        self.stopped_threads = {}

    def get_running_thread(self, name: str):
        return self.running_threads[name]

    def add_thread(self, thread: Thread):
        self.running_threads[thread.name] = thread
        self.running_threads[thread.name].start()

    def stop_thread(self, name: str):
        self.stopped_threads[name] = self.running_threads.pop(name)

    def is_all_stopped(self):
        return len(self.running_threads) == 0

    def clear(self):
        self.running_threads.clear()
        self.stopped_threads.clear()