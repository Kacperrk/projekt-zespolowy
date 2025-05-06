import random
from itertools import combinations
from typing import Optional

from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QLineEdit, QPushButton, QMessageBox, QSplitter, QSizePolicy
)
from PyQt5.QtCore import Qt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from matplotlib.axes import Axes

from algorytm import znajdz_najlepsza_trase_genetyczny
from algorytm import znajdz_najlepsza_trase_najblizszego_sasiada


class KomiwojazerApp(QWidget):
    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle("Problem Komiwojażera - PyQt5")
        self.resize(1200, 800)

        self.miasta: dict[str, tuple[float, float]] = {}
        self.drogi: list[tuple[str, str]] = []

        self.nazwa_input = QLineEdit()
        self.x_input = QLineEdit()
        self.y_input = QLineEdit()
        self.miasto1_input = QLineEdit()
        self.miasto2_input = QLineEdit()

        self.figure = Figure()
        self.ax: Axes = self.figure.add_subplot(111)
        self.canvas = FigureCanvas(self.figure)

        self.init_ui()

    def init_ui(self) -> None:
        layout = QHBoxLayout()
        controls = QVBoxLayout()

        self.setStyleSheet("""
            QLabel { font-weight: bold; }
        """)

        def configure_widget(widget):
            size_policy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
            widget.setSizePolicy(size_policy)

        controls.addWidget(QLabel("Nazwa miasta:"))
        configure_widget(self.nazwa_input)
        controls.addWidget(self.nazwa_input)

        controls.addWidget(QLabel("Współrzędna X:"))
        configure_widget(self.x_input)
        controls.addWidget(self.x_input)

        controls.addWidget(QLabel("Współrzędna Y:"))
        configure_widget(self.y_input)
        controls.addWidget(self.y_input)

        def make_button(text: str, handler, style: str = "") -> QPushButton:
            btn = QPushButton(text)
            btn.setStyleSheet(style)
            btn.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
            btn.setMinimumHeight(30)
            # noinspection PyUnresolvedReferences
            btn.clicked.connect(handler)
            return btn

        controls.addWidget(make_button("Dodaj miasto", self.dodaj_miasto, "background-color: #4CAF50; color: white;"))

        controls.addWidget(QLabel("Połącz miasta (podaj 2 nazwy):"))
        configure_widget(self.miasto1_input)
        controls.addWidget(self.miasto1_input)
        configure_widget(self.miasto2_input)
        controls.addWidget(self.miasto2_input)

        controls.addWidget(make_button("Połącz miasta", self.polacz_miasta, "background-color: #2196F3; color: white;"))
        controls.addWidget(make_button("Połącz wszystkie miasta", self.polacz_wszystkie_miasta, "background-color: #2196F3; color: white;"))
        controls.addWidget(make_button("Wyczyść miasta", self.wyczysc_miasta, "background-color: #FF5733; color: white;"))
        controls.addWidget(make_button("Wyczyść połączenia", self.wyczysc_polaczenia, "background-color: #FF5733; color: white;"))
        controls.addWidget(make_button("Generuj 5 losowych miast", self.generuj_losowe_miasta, "background-color: #FFEB3B;"))
        controls.addWidget(make_button("Znajdź optymalną trasę (genetyczny)", lambda: znajdz_najlepsza_trase_genetyczny(self), "background-color: #B04CAD; color: white;"))
        controls.addWidget(make_button("Znajdź optymalną trasę (najbliższego sąsiada)", lambda: znajdz_najlepsza_trase_najblizszego_sasiada(self), "background-color: #B04CAD; color: white;"))
        controls.addWidget(make_button("Zapisz stan projektu", self.zapisz_stan_projektu, "background-color: #4CAF50; color: white;"))
        controls.addWidget(make_button("Wczytaj stan projektu", self.wczytaj_stan_projektu, "background-color: #4CAF50; color: white;"))

        # Dodaj stretch na koniec, by layout był rozciągliwy
        controls.addStretch()

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

    def polacz_miasta(self) -> None:
        miasto1 = self.miasto1_input.text().strip()
        miasto2 = self.miasto2_input.text().strip()

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

        miasta_list = list(self.miasta.keys())
        for miasto1, miasto2 in combinations(miasta_list, 2):
            if (miasto1, miasto2) not in self.drogi and (miasto2, miasto1) not in self.drogi:
                self.drogi.append((miasto1, miasto2))
        self.rysuj_mape()

    def wyczysc_miasta(self) -> None:
        self.drogi.clear()
        self.miasta.clear()
        self.rysuj_mape()

    def wyczysc_polaczenia(self) -> None:
        if not self.drogi:
            QMessageBox.critical(self, "Błąd", "Brak połączeń do wyczyszczenia.")
            return

        self.drogi.clear()
        self.rysuj_mape()

    def generuj_losowe_miasta(self) -> None:
        start_index = len(self.miasta) + 1
        for i in range(5):
            nazwa = f"Miasto{start_index + i}"
            x = random.randint(0, 50)
            y = random.randint(0, 50)
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
            self.ax.plot(x, y, 'ro', markersize=12, markeredgewidth=2, markeredgecolor='black')
            self.ax.text(x + 0.3, y + 0.3, nazwa, fontsize=12, color='black', fontweight='bold')

        for miasto1, miasto2 in self.drogi:
            x1, y1 = self.miasta[miasto1]
            x2, y2 = self.miasta[miasto2]
            self.ax.plot([x1, x2], [y1, y2], 'darkblue', linewidth=2)

        if najlepsza_trasa:
            wspolrzedne = [self.miasta[n] for n in najlepsza_trasa]
            wspolrzedne.append(wspolrzedne[0])
            x_coords, y_coords = zip(*wspolrzedne)
            self.ax.plot(x_coords, y_coords, 'g-', linewidth=2)

        self.ax.set_title("Mapa miast i połączeń", fontsize=16)
        self.ax.set_xlabel("X", fontsize=12)
        self.ax.set_ylabel("Y", fontsize=12)

        self.canvas.draw()
