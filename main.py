import sys
from PyQt5.QtWidgets import QApplication
from gui import KomiwojazerApp

def main() -> None:
    app = QApplication(sys.argv)  # Tworzenie aplikacji
    main_window = KomiwojazerApp()  # Tworzenie głównego okna
    main_window.resize(1000, 600)
    main_window.show()
    app.exec_()  # Uruchomienie głównej pętli aplikacji

if __name__ == "__main__":
    main()
