import os
import sys

import flet as ft

sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from src.ui.main_page import MainWindow


def main(page: ft.Page):
    main_window: ft.Control = MainWindow()
    page.add(ft.SafeArea(main_window))


if __name__ == "__main__":
    ft.run(main)
