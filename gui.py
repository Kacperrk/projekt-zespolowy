import random
from itertools import combinations
from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QLineEdit, QPushButton, QMessageBox, QSplitter
)
from PyQt5.QtCore import Qt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import matplotlib.pyplot as plt
from algorytm import znajdz_najlepsza_trase_genetyczny
from algorytm import znajdz_najlepsza_trase_najblizszego_sasiada


class KomiwojazerApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Problem Komiwojażera - PyQt5")
        self.resize(1200, 800)  # Większe okno startowe
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

        # Styl globalny (większe czcionki i padding)
        self.setStyleSheet("""
            QWidget {
                font-size: 14pt;
            }
            QLineEdit {
                padding: 6px;
                font-size: 14pt;
            }
            QPushButton {
                padding: 10px;
                font-size: 14pt;
            }
            QLabel {
                font-size: 14pt;
                font-weight: bold;
            }
        """)

        # Pole do wpisania miasta
        controls.addWidget(QLabel("Nazwa miasta:"))
        controls.addWidget(self.nazwa_input)

        controls.addWidget(QLabel("Współrzędna X:"))
        controls.addWidget(self.x_input)

        controls.addWidget(QLabel("Współrzędna Y:"))
        controls.addWidget(self.y_input)

        # Przycisk dodawania miasta
        dodaj_btn = QPushButton("Dodaj miasto")
        dodaj_btn.setStyleSheet("background-color: #4CAF50; color: white;")
        dodaj_btn.clicked.connect(self.dodaj_miasto)
        controls.addWidget(dodaj_btn)

        controls.addWidget(QLabel("Połącz miasta (podaj 2 nazwy):"))
        controls.addWidget(self.m1_input)
        controls.addWidget(self.m2_input)

        polacz_btn = QPushButton("Połącz miasta")
        polacz_btn.setStyleSheet("background-color: #2196F3; color: white;")
        polacz_btn.clicked.connect(self.polacz_miasta)
        controls.addWidget(polacz_btn)

        polacz_wszystkie_btn = QPushButton("Połącz wszystkie miasta")
        polacz_wszystkie_btn.setStyleSheet("background-color: #2196F3; color: white;")
        polacz_wszystkie_btn.clicked.connect(self.polacz_wszystkie_miasta)
        controls.addWidget(polacz_wszystkie_btn)

        wyczysc_miasta_btn = QPushButton("Wyczyść miasta")
        wyczysc_miasta_btn.setStyleSheet("background-color: #FF5733; color: white;")
        wyczysc_miasta_btn.clicked.connect(self.wyczysc_miasta)
        controls.addWidget(wyczysc_miasta_btn)

        wyczysc_btn = QPushButton("Wyczyść połączenia")
        wyczysc_btn.setStyleSheet("background-color: #FF5733; color: white;")
        wyczysc_btn.clicked.connect(self.wyczysc_polaczenia)
        controls.addWidget(wyczysc_btn)

        generuj_btn = QPushButton("Generuj 5 losowych miast")
        generuj_btn.setStyleSheet("background-color: #FFEB3B;")
        generuj_btn.clicked.connect(self.generuj_losowe_miasta)
        controls.addWidget(generuj_btn)

        znajdz_btn = QPushButton("Znajdź optymalną trasę (genetyczny)")
        znajdz_btn.setStyleSheet("background-color: #B04CAD; color: white;")
        znajdz_btn.clicked.connect(lambda: znajdz_najlepsza_trase_genetyczny(self))
        controls.addWidget(znajdz_btn)

        znajdz_btn2 = QPushButton("Znajdź optymalną trasę (najbliższego sąsiada)")
        znajdz_btn2.setStyleSheet("background-color: #B04CAD; color: white;")
        znajdz_btn2.clicked.connect(lambda: znajdz_najlepsza_trase_najblizszego_sasiada(self))
        controls.addWidget(znajdz_btn2)

        zapis_btn = QPushButton("Zapisz stan projektu")
        zapis_btn.setStyleSheet("background-color: #4CAF50; color: white;")
        zapis_btn.clicked.connect(self.zapisz_stan_projektu)
        controls.addWidget(zapis_btn)

        wczytaj_btn = QPushButton("Wczytaj stan projektu")
        wczytaj_btn.setStyleSheet("background-color: #4CAF50; color: white;")
        wczytaj_btn.clicked.connect(self.wczytaj_stan_projektu)
        controls.addWidget(wczytaj_btn)

        # Podział GUI na lewy panel (kontrolki) i prawy (mapa)
        splitter = QSplitter(Qt.Horizontal)
        controls_widget = QWidget()
        controls_widget.setLayout(controls)

        splitter.addWidget(controls_widget)
        splitter.addWidget(self.canvas)
        splitter.setSizes([400, 800])  # Zwiększenie szerokości panelu bocznego

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

    def zapisz_stan_projektu(self):
        try:
            with open("stan_projektu.txt", "w") as f:
                for nazwa, (x, y) in self.miasta.items():
                    f.write(f"{nazwa},{x},{y}\n")
                for m1, m2 in self.drogi:
                    f.write(f"{m1},{m2}\n")
        except Exception as e:
            QMessageBox.critical(self, "Błąd", f"Nie udało się zapisać stanu projektu: {str(e)}")

    def wczytaj_stan_projektu(self):
        try:
            with open("stan_projektu.txt", "r") as f:
                self.miasta.clear()
                self.drogi.clear()
                for line in f:
                    parts = line.strip().split(",")
                    if len(parts) == 3:
                        nazwa, x, y = parts
                        self.miasta[nazwa] = (float(x), float(y))
                    elif len(parts) == 2:
                        m1, m2 = parts
                        self.drogi.append((m1, m2))
            self.rysuj_mape()
        except Exception as e:
            QMessageBox.critical(self, "Błąd", f"Nie udało się wczytać stanu projektu: {str(e)}")

    def rysuj_mape(self, najlepsza_trasa=None):
        self.ax.clear()

        for nazwa, (x, y) in self.miasta.items():
            self.ax.plot(x, y, 'ro', markersize=12, markeredgewidth=2,
                         markeredgecolor='black')
            self.ax.text(x + 0.3, y + 0.3, nazwa, fontsize=12, color='black',
                         fontweight='bold')

        for m1, m2 in self.drogi:
            x1, y1 = self.miasta[m1]
            x2, y2 = self.miasta[m2]
            self.ax.plot([x1, x2], [y1, y2], 'darkblue', linewidth=3)

        if najlepsza_trasa:
            for i in range(len(najlepsza_trasa)):
                m1 = najlepsza_trasa[i]
                m2 = najlepsza_trasa[(i + 1) % len(najlepsza_trasa)]
                x1, y1 = self.miasta[m1]
                x2, y2 = self.miasta[m2]
                self.ax.plot([x1, x2], [y1, y2], 'limegreen', linewidth=4)

        self.ax.set_title("Mapa miast i trasa", fontsize=14, fontweight='bold')
        self.ax.set_xlabel("X", fontsize=12)
        self.ax.set_ylabel("Y", fontsize=12)
        self.ax.grid(True, linestyle='--', alpha=0.5)
        self.canvas.draw()
