
from PyQt5.QtWidgets import QApplication
import sys
from gui import KomiwojazerApp

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = KomiwojazerApp()
    window.resize(1000, 600)
    window.show()
    sys.exit(app.exec_())
