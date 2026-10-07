import psutil

from src.models.base_model import Metric


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
        mem = psutil.virtual_memory()
        self._total = mem.total
        self._used = mem.used
        self._free = mem.free
        self._value = mem.percent
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
        disk = psutil.disk_usage("C:\\")
        self._total = disk.total
        self._used = disk.used
        self._free = disk.free
        self._value = disk.percent
        self.remember()

    def info(self):
        return f"Disk: {self._used/1024/1024/1024:.1f} GB / {self._total/1024/1024/1024:.1f} GB ({self._free/1024/1024/1024:.1f} GB free)"


class network_metric(Metric):
    def __init__(self):
        super().__init__("Network")
        self._bytes_sent = 0
        self._bytes_recv = 0

    def update(self):
        net = psutil.net_io_counters()
        self._bytes_sent = net.bytes_sent
        self._bytes_recv = net.bytes_recv
        self._value = self._bytes_recv / (1024 ** 2)
        self.remember()

    def info(self):
        return f"Network: {self._bytes_sent/1024/1024/1024:.1f} GB / {self._bytes_recv/1024/1024/1024:.1f} GB"
