from metrics import cpu_metric, memory_metric, disk_metric, network_metric
import flet as ft
import time
import threading
import psutil


def Monitor(page: ft.Page):
    """Тут делаем отображение окна"""
    page.title = "Monitor"
    page.window_width = 600
    page.window_height = 800
    page.scroll = ft.ScrollMode.AUTO
    page.bgcolor = "white"
    page.theme_mode = ft.ThemeMode.LIGHT
    page.window_resizable = False
    page.window_maximizable = False
    page.window_minimizable = False
    page.window_draggable = True
    page.window_decorated = True
    items = [
        (cpu_metric(), ft.Text("CPU", color="black")),
        (memory_metric(), ft.Text("Memory", color="black")),
        (disk_metric(), ft.Text("Disk", color="black")),
        (network_metric(), ft.Text("Network", color="black")),
    ]
    charts = []
    for metric, label in items:
        bars = ft.Row(spacing=2, vertical_alignment=ft.CrossAxisAlignment.END, expand=True)
        charts.append(bars)
        page.add(
            label,
            ft.Container(
                height=140,
                bgcolor="white",
                border=ft.Border.all(1, "#bdbdbd"),
                padding=8,
                content=ft.Row(
                    [
                        ft.Column(
                            [
                                ft.Text("100", size=11, color="black"),
                                ft.Text("50", size=11, color="black"),
                                ft.Text("0", size=11, color="black"),
                            ],
                            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                            height=110,
                        ),
                        bars,
                    ],
                    vertical_alignment=ft.CrossAxisAlignment.END,
                ),
            ),
        )

    def draw(bars, history):
        """Столбики по последним точкам"""
        tail = history[-60:]
        bars.controls.clear()
        peak = 100
        for moment, value in tail:
            if value > peak:
                peak = value
        for moment, value in tail:
            bars.controls.append(
                ft.Container(
                    width=5,
                    height=max(float(value) / peak * 100, 1),
                    bgcolor="#1976d2",
                )
            )

    def refresh():
        """Тут обновляются метрики"""
        for i in range(len(items)):
            metric, label = items[i]
            metric.update()
            label.value = metric.info()
            draw(charts[i], metric._history)
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

