from src.ui.main_page import MainWindow


def test_main_window():
    window = MainWindow()
    assert len(window.controls) == 8
