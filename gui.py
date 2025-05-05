import random
from itertools import combinations
from typing import Optional

from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QLineEdit, QPushButton, QMessageBox, QSplitter
)
from PyQt5.QtCore import Qt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from matplotlib.axes import Axes

from algorytm import znajdz_najlepsza_trase_genetyczny
from algorytm import znajdz_najlepsza_trase_najblizszego_sasiada


class KomiwojazerApp(QWidget):
    miasta: dict[str, tuple[float, float]]
    drogi: list[tuple[str, str]]

    nazwa_input: QLineEdit
    x_input: QLineEdit
    y_input: QLineEdit
    miasto1_input: QLineEdit
    miasto2_input: QLineEdit

    figure: Figure
    ax: Axes
    canvas: FigureCanvas

    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle("Problem Komiwojażera - PyQt5")
        self.resize(1200, 800)
        self.miasta = {}
        self.drogi = []

        self.nazwa_input = QLineEdit()
        self.x_input = QLineEdit()
        self.y_input = QLineEdit()
        self.miasto1_input = QLineEdit()
        self.miasto2_input = QLineEdit()

        self.figure, self.ax = plt.subplots()
        self.canvas = FigureCanvas(self.figure)

        self.init_ui()

    def init_ui(self) -> None:
        layout = QHBoxLayout()
        controls = QVBoxLayout()

        self.setStyleSheet("""
            QWidget { font-size: 14pt; }
            QLineEdit { padding: 6px; font-size: 14pt; }
            QPushButton { padding: 10px; font-size: 14pt; }
            QLabel { font-size: 14pt; font-weight: bold; }
        """)

        controls.addWidget(QLabel("Nazwa miasta:"))
        controls.addWidget(self.nazwa_input)

        controls.addWidget(QLabel("Współrzędna X:"))
        controls.addWidget(self.x_input)

        controls.addWidget(QLabel("Współrzędna Y:"))
        controls.addWidget(self.y_input)

        dodaj_btn = QPushButton("Dodaj miasto")
        dodaj_btn.setStyleSheet("background-color: #4CAF50; color: white;")
        dodaj_btn.clicked.connect(self.dodaj_miasto)
        controls.addWidget(dodaj_btn)

        controls.addWidget(QLabel("Połącz miasta (podaj 2 nazwy):"))
        controls.addWidget(self.miasto1_input)
        controls.addWidget(self.miasto2_input)

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

        splitter = QSplitter(Qt.Horizontal)
        controls_widget = QWidget()
        controls_widget.setLayout(controls)

        splitter.addWidget(controls_widget)
        splitter.addWidget(self.canvas)
        splitter.setSizes([400, 800])

        layout.addWidget(splitter)
        self.setLayout(layout)
        self.rysuj_mape()

    def dodaj_miasto(self) -> None:
        nazwa: str = self.nazwa_input.text().strip()
        try:
            x: float = float(self.x_input.text().strip())
            y: float = float(self.y_input.text().strip())
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

    def polacz_miasta(self) -> None:
        miasto1: str = self.miasto1_input.text().strip()
        miasto2: str = self.miasto2_input.text().strip()

        if miasto1 == miasto2:
            QMessageBox.warning(self, "Uwaga", "Nie można połączyć miasta z samym sobą.")
            return

        if miasto1 in self.miasta and miasto2 in self.miasta:
            if (miasto1, miasto2) not in self.drogi and (miasto2, miasto1) not in self.drogi:
                self.drogi.append((miasto1, miasto2))
                self.rysuj_mape()
            else:
                QMessageBox.information(self, "Info", "Miasta są już połączone.")
        else:
            QMessageBox.critical(self, "Błąd", "Podane miasta muszą istnieć.")

        self.miasto1_input.clear()
        self.miasto2_input.clear()

    def polacz_wszystkie_miasta(self) -> None:
        if not self.miasta:
            QMessageBox.critical(self, "Błąd", "Brak miast do połączenia. Dodaj miasta najpierw.")
            return

        miasta_list: list[str] = list(self.miasta.keys())
        for miasto1, miasto2 in combinations(miasta_list, 2):
            if (miasto1, miasto2) not in self.drogi and (miasto2, miasto1) not in self.drogi:
                self.drogi.append((miasto1, miasto2))
        self.rysuj_mape()

    def wyczysc_miasta(self) -> None:
        self.drogi.clear()
        self.miasta.clear()
        self.rysuj_mape()

    def wyczysc_polaczenia(self) -> None:
        self.drogi.clear()
        self.rysuj_mape()

    def generuj_losowe_miasta(self) -> None:
        start_index: int = len(self.miasta) + 1
        for i in range(5):
            nazwa: str = f"Miasto{start_index + i}"
            x: int = random.randint(0, 50)
            y: int = random.randint(0, 50)
            self.miasta[nazwa] = (x, y)
        self.drogi.clear()
        self.rysuj_mape()

    def zapisz_stan_projektu(self) -> None:
        try:
            with open("stan_projektu.txt", "w") as f:
                for nazwa, (x, y) in self.miasta.items():
                    f.write(f"{nazwa},{x},{y}\n")
                for miasto1, miasto2 in self.drogi:
                    f.write(f"{miasto1},{miasto2}\n")
        except Exception as e:
            QMessageBox.critical(self, "Błąd", f"Nie udało się zapisać stanu projektu: {str(e)}")

    def wczytaj_stan_projektu(self) -> None:
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
                        miasto1, miasto2 = parts
                        self.drogi.append((miasto1, miasto2))
            self.rysuj_mape()
        except Exception as e:
            QMessageBox.critical(self, "Błąd", f"Nie udało się wczytać stanu projektu: {str(e)}")

    def rysuj_mape(self, najlepsza_trasa: Optional[list[str]] = None) -> None:
        self.ax.clear()

        for nazwa, (x, y) in self.miasta.items():
            self.ax.plot(x, y, 'ro', markersize=12, markeredgewidth=2,
                         markeredgecolor='black')
            self.ax.text(x + 0.3, y + 0.3, nazwa, fontsize=12, color='black',
                         fontweight='bold')

        for miasto1, miasto2 in self.drogi:
            x1, y1 = self.miasta[miasto1]
            x2, y2 = self.miasta[miasto2]
            self.ax.plot([x1, x2], [y1, y2], 'darkblue', linewidth=2)

        if najlepsza_trasa:
            najlepsza_trasa_koord = [self.miasta[miasto] for miasto in najlepsza_trasa]
            najlepsza_trasa_koord.append(najlepsza_trasa_koord[0])  # Zamykamy trasę
            x_coords, y_coords = zip(*najlepsza_trasa_koord)
            self.ax.plot(x_coords, y_coords, 'g-', linewidth=2)

        self.ax.set_title("Mapa miast i połączeń", fontsize=16)
        self.ax.set_xlabel("X", fontsize=12)
        self.ax.set_ylabel("Y", fontsize=12)

        self.canvas.draw()
