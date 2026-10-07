from abc import ABC
import time


class Metric(ABC):
    def __init__(self, name):
        self._name = name
        self._value = 0
        self._history = []
        self._keep_seconds = 3600

    def remember(self):
        moment = time.time()
        self._history.append((moment, self._value))
        oldest = moment - self._keep_seconds
        while self._history and self._history[0][0] < oldest:
            del self._history[0]
