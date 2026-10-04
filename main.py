from metrics import Metric
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
    page.add(ft.Text("Hello, World!"))



def main(page: ft.Page): 
    Monitor(page)

#def main():
#    check_metrics = Metric('проверка метрики')
#    print(check_metrics)


if __name__== "__main__":
    ft.run(main)

