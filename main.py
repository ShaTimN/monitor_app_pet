from metrics import cpu_metric, memory_metric, disk_metric, network_metric
import flet as ft



def Monitor(page: ft.Page):
    page.title = "Monitor"
    page.window_width = 600
    page.window_height = 400
    page.window_resizable = False
    page.window_maximizable = False
    page.window_minimizable = False
    page.window_draggable = True
    page.window_decorated = True
    cpu = cpu_metric()
    cpu.update()
    memory = memory_metric()
    memory.update()
    disk = disk_metric()
    disk.update()
    network = network_metric()
    network.update()
    page.add(ft.Text("Hello, World!"))
    page.add(ft.Text(cpu.info()))
    page.add(ft.Text(memory.info()))
    page.add(ft.Text(disk.info()))
    page.add(ft.Text(network.info()))



def main(page: ft.Page): 
    Monitor(page)

#def main():
#    check_metrics = Metric('проверка метрики')
#    print(check_metrics)


if __name__== "__main__":
    ft.run(main)

