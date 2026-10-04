from metrics import cpu_metric, memory_metric, disk_metric, network_metric
import flet as ft
import time
import threading
import psutil


def Monitor(page: ft.Page):
    """Тут делаем отображение окна"""
    page.title = "Monitor"
    page.window_width = 600
    page.window_height = 400
    page.window_resizable = False
    page.window_maximizable = False
    page.window_minimizable = False
    page.window_draggable = True
    page.window_decorated = True
    items = [
        (cpu_metric(), ft.Text("CPU")),
        (memory_metric(), ft.Text("Memory")),
        (disk_metric(), ft.Text("Disk")),
        (network_metric(), ft.Text("Network")),
    ]
    for metric, label in items:
        page.add(label)

    def refresh():
        """Тут обновляются метрики"""
        for metric, label in items:
            metric.update()
            label.value = metric.info()
        page.update()

    def loop():
        """Тут запускаем цикл обновления метрик"""
        while True:
            try:
                refresh()
            except RuntimeError:
                break
            time.sleep(0.1)
    threading.Thread(target=loop, daemon=True).start()



def main(page: ft.Page): 
    """Тут запускаем приложение"""
    monitor = Monitor(page)
    net = psutil.net_io_counters()
    bytes_sent = net.bytes_sent
    bytes_recv = net.bytes_recv

#def main():
#    check_metrics = Metric('проверка метрики')
#    print(check_metrics)


if __name__== "__main__":
    """Тут понятно"""
    ft.run(main)

