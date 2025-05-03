import sys
from typing import NoReturn
from PyQt5.QtWidgets import QApplication
from gui import KomiwojazerApp


def create_application() -> QApplication:
    return QApplication(sys.argv)


def main() -> NoReturn:
    app: QApplication = create_application()
    main_window: KomiwojazerApp = KomiwojazerApp()
    main_window.resize(1000, 600)
    main_window.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
