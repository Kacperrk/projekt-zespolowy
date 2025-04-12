import sys
from PyQt5.QtWidgets import QApplication
from gui import KomiwojazerApp  # Import Twojej klasy GUI z gui.py

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = KomiwojazerApp()  # Tworzymy instancję aplikacji
    window.resize(1000, 600)  # Ustawiamy rozmiar okna
    window.show()  # Wyświetlamy okno
    sys.exit(app.exec_())  # Uruchamiamy aplikację
