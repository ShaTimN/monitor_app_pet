import time
import threading

import flet as ft

from src.models.metrics import cpu_metric, memory_metric, disk_metric, network_metric


class MainWindow(ft.Column):
    """Тут делаем отображение окна"""

    def __init__(self):
        super().__init__(spacing=8)
        self.items = [
            (cpu_metric(), ft.Text("CPU", color="black")),
            (memory_metric(), ft.Text("Memory", color="black")),
            (disk_metric(), ft.Text("Disk", color="black")),
            (network_metric(), ft.Text("Network", color="black")),
        ]
        self.charts = []
        for metric, label in self.items:
            bars = ft.Row(spacing=2, vertical_alignment=ft.CrossAxisAlignment.END, expand=True)
            self.charts.append(bars)
            self.controls.append(label)
            self.controls.append(
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
                )
            )

    def did_mount(self):
        page = self.page
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
        threading.Thread(target=self.loop, daemon=True).start()

    def draw(self, bars, history):
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

    def refresh(self):
        """Тут обновляются метрики"""
        for i in range(len(self.items)):
            metric, label = self.items[i]
            metric.update()
            label.value = metric.info()
            self.draw(self.charts[i], metric._history)
        self.page.update()

    def loop(self):
        """Тут запускаем цикл обновления метрик"""
        while True:
            try:
                self.refresh()
            except RuntimeError:
                break
            time.sleep(0.1)
