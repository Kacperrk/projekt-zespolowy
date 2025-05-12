import sys
from PyQt5.QtWidgets import QApplication
from gui import KomiwojazerApp


def main() -> None:
    app: QApplication = QApplication(sys.argv)
    main_window: KomiwojazerApp = KomiwojazerApp()
    main_window.resize(1000, 600)
    main_window.show()
    app.exec_()


if __name__ == "__main__":
    main()
