import sys
from PyQt5.QtWidgets import QApplication
from gui import KomiwojazerApp

def main():
    app = QApplication(sys.argv)
    window = KomiwojazerApp()
    window.resize(1000, 600)
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
