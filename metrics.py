from abc import ABC
import time
import psutil


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

class cpu_metric(Metric):
    def __init__(self):
        super().__init__("CPU")
        self._freq = 0
        
    def update(self):
        self._value = psutil.cpu_percent(interval=None)
        freq = psutil.cpu_freq()
        if freq:
            self._freq = freq.current
        else:
            self._freq = 0
        self.remember()

    def info(self):
        return f"CPU: {self._value}% ({self._freq} MHz)"

class memory_metric(Metric):
    def __init__(self):
        super().__init__("Memory")
        self._total = 0
        self._used = 0
        self._free = 0
    
    def update(self):
        self._total = psutil.virtual_memory().total
        self._used = psutil.virtual_memory().used
        self._free = psutil.virtual_memory().free
        self.remember()

    def info(self):
        return f"Memory: {self._used/1024/1024/1024:.1f} GB / {self._total/1024/1024/1024:.1f} GB ({self._free/1024/1024/1024:.1f} GB free)"

class disk_metric(Metric):
    def __init__(self):
        super().__init__("Disk")
        self._total = 0
        self._used = 0
        self._free = 0
    
    def update(self):
        self._total = psutil.disk_usage("C:\\").total
        self._used = psutil.disk_usage("C:\\").used
        self._free = psutil.disk_usage("C:\\").free
        self.remember()

    def info(self):
        return f"Disk: {self._used/1024/1024/1024:.1f} GB / {self._total/1024/1024/1024:.1f} GB ({self._free/1024/1024/1024:.1f} GB free)"

class network_metric(Metric):
    def __init__(self):
        super().__init__("Network")
        self._bytes_sent = 0
        self._bytes_recv = 0
    
    def update(self):
        bytes_sent, bytes_recv = psutil.net_io_counters().bytes_sent, psutil.net_io_counters().bytes_recv
        self._bytes_sent += bytes_sent
        self._bytes_recv += bytes_recv
        self.remember()

    def info(self):
        return f"Network: {self._bytes_sent/1024/1024/1024:.1f} GB / {self._bytes_recv/1024/1024/1024:.1f} GB"

#if __name__ == "__main__":
#    cpu = cpu_metric()
#    cpu.update()
#    print(cpu.info(), len(cpu._history))
#    memory = memory_metric()
#    memory.update()
#    print(memory.info(), len(memory._history))
#    disk = disk_metric()
#    disk.update()
#    print(disk.info(), len(disk._history))
#    network = network_metric()
#    network.update()
#    print(network.info(), len(network._history))