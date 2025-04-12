
from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QLineEdit, QPushButton, QMessageBox, QSplitter
)
from PyQt5.QtCore import Qt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import matplotlib.pyplot as plt
from itertools import combinations
import random
from algorytm import znajdz_najlepsza_trase


class KomiwojazerApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Problem Komiwojażera - PyQt5")
        self.miasta = {}
        self.drogi = []

        self.nazwa_input = QLineEdit()
        self.x_input = QLineEdit()
        self.y_input = QLineEdit()
        self.m1_input = QLineEdit()
        self.m2_input = QLineEdit()

        self.figure, self.ax = plt.subplots()
        self.canvas = FigureCanvas(self.figure)

        self.init_ui()

    def init_ui(self):
        layout = QHBoxLayout()
        controls = QVBoxLayout()
        controls.addWidget(QLabel("Nazwa miasta:"))
        controls.addWidget(self.nazwa_input)
        controls.addWidget(QLabel("Współrzędna X:"))
        controls.addWidget(self.x_input)
        controls.addWidget(QLabel("Współrzędna Y:"))
        controls.addWidget(self.y_input)

        dodaj_btn = QPushButton("Dodaj miasto")
        dodaj_btn.clicked.connect(self.dodaj_miasto)
        controls.addWidget(dodaj_btn)

        controls.addWidget(QLabel("Połącz miasta (podaj 2 nazwy):"))
        controls.addWidget(self.m1_input)
        controls.addWidget(self.m2_input)

        polacz_btn = QPushButton("Połącz miasta")
        polacz_btn.clicked.connect(self.polacz_miasta)
        controls.addWidget(polacz_btn)

        polacz_wszystkie_btn = QPushButton("Połącz wszystkie miasta")
        polacz_wszystkie_btn.clicked.connect(self.polacz_wszystkie_miasta)
        controls.addWidget(polacz_wszystkie_btn)

        wyczysc_miasta_btn = QPushButton("Wyczyść miasta")
        wyczysc_miasta_btn.clicked.connect(self.wyczysc_miasta)
        controls.addWidget(wyczysc_miasta_btn)

        wyczysc_btn = QPushButton("Wyczyść połączenia")
        wyczysc_btn.clicked.connect(self.wyczysc_polaczenia)
        controls.addWidget(wyczysc_btn)

        generuj_btn = QPushButton("Generuj 5 losowych miast")
        generuj_btn.clicked.connect(self.generuj_losowe_miasta)
        controls.addWidget(generuj_btn)

        znajdz_btn = QPushButton("Znajdź optymalną trasę")
        znajdz_btn.clicked.connect(lambda: znajdz_najlepsza_trase(self))
        controls.addWidget(znajdz_btn)

        splitter = QSplitter(Qt.Horizontal)
        controls_widget = QWidget()
        controls_widget.setLayout(controls)
        splitter.addWidget(controls_widget)
        splitter.addWidget(self.canvas)
        splitter.setStretchFactor(0, 1)
        splitter.setStretchFactor(1, 4)

        layout.addWidget(splitter)
        self.setLayout(layout)
        self.rysuj_mape()

    def dodaj_miasto(self):
        nazwa = self.nazwa_input.text().strip()
        try:
            x = float(self.x_input.text().strip())
            y = float(self.y_input.text().strip())
        except ValueError:
            QMessageBox.critical(self, "Błąd", "Wprowadź poprawne współrzędne.")
            return

        if nazwa in self.miasta:
            QMessageBox.warning(self, "Uwaga", "Miasto o tej nazwie już istnieje.")
            return

        self.miasta[nazwa] = (x, y)
        self.drogi.clear()
        self.nazwa_input.clear()
        self.x_input.clear()
        self.y_input.clear()
        self.rysuj_mape()

    def polacz_miasta(self):
        m1 = self.m1_input.text().strip()
        m2 = self.m2_input.text().strip()

        if m1 == m2:
            QMessageBox.warning(self, "Uwaga", "Nie można połączyć miasta z samym sobą.")
            return

        if m1 in self.miasta and m2 in self.miasta:
            if (m1, m2) not in self.drogi and (m2, m1) not in self.drogi:
                self.drogi.append((m1, m2))
                self.rysuj_mape()
            else:
                QMessageBox.information(self, "Info", "Miasta są już połączone.")
        else:
            QMessageBox.critical(self, "Błąd", "Podane miasta muszą istnieć.")

        self.m1_input.clear()
        self.m2_input.clear()

    def polacz_wszystkie_miasta(self):
        miasta_list = list(self.miasta.keys())
        for m1, m2 in combinations(miasta_list, 2):
            if (m1, m2) not in self.drogi and (m2, m1) not in self.drogi:
                self.drogi.append((m1, m2))
        self.rysuj_mape()

    def wyczysc_miasta(self):
        self.drogi.clear()
        self.miasta.clear()
        self.rysuj_mape()

    def wyczysc_polaczenia(self):
        self.drogi.clear()
        self.rysuj_mape()

    def generuj_losowe_miasta(self):
        start_index = len(self.miasta) + 1
        for i in range(5):
            nazwa = f"Miasto{start_index + i}"
            x = random.randint(0, 50)
            y = random.randint(0, 50)
            self.miasta[nazwa] = (x, y)
        self.drogi.clear()
        self.rysuj_mape()

    def rysuj_mape(self, najlepsza_trasa=None):
        self.ax.clear()
        for nazwa, (x, y) in self.miasta.items():
            self.ax.plot(x, y, 'ro')
            self.ax.text(x + 0.2, y + 0.2, nazwa)

        for m1, m2 in self.drogi:
            x1, y1 = self.miasta[m1]
            x2, y2 = self.miasta[m2]
            self.ax.plot([x1, x2], [y1, y2], 'b--')

        if najlepsza_trasa:
            for i in range(len(najlepsza_trasa)):
                m1 = najlepsza_trasa[i]
                m2 = najlepsza_trasa[(i + 1) % len(najlepsza_trasa)]
                x1, y1 = self.miasta[m1]
                x2, y2 = self.miasta[m2]
                self.ax.plot([x1, x2], [y1, y2], 'g-', linewidth=4)

        self.ax.set_title("Mapa miast i trasa")
        self.ax.set_xlabel("X")
        self.ax.set_ylabel("Y")
        self.ax.grid(True)
        self.canvas.draw()
