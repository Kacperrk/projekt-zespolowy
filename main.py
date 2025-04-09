import sys
import random
import math
from itertools import combinations
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import matplotlib.pyplot as plt
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QLineEdit, QPushButton, QMessageBox
)


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
        # noinspection PyUnresolvedReferences
        dodaj_btn.clicked.connect(self.dodaj_miasto)
        controls.addWidget(dodaj_btn)

        controls.addWidget(QLabel("Połącz miasta (podaj 2 nazwy):"))
        controls.addWidget(self.m1_input)
        controls.addWidget(self.m2_input)

        polacz_btn = QPushButton("Połącz miasta")
        # noinspection PyUnresolvedReferences
        polacz_btn.clicked.connect(self.polacz_miasta)
        controls.addWidget(polacz_btn)

        polacz_wszystkie_btn = QPushButton("Połącz wszystkie miasta")
        # noinspection PyUnresolvedReferences
        polacz_wszystkie_btn.clicked.connect(self.polacz_wszystkie_miasta)
        controls.addWidget(polacz_wszystkie_btn)

        wyczysc_miasta_btn = QPushButton("Wyczyść miasta")
        # noinspection PyUnresolvedReferences
        wyczysc_miasta_btn.clicked.connect(self.wyczysc_miasta)
        controls.addWidget(wyczysc_miasta_btn)

        wyczysc_btn = QPushButton("Wyczyść połączenia")
        # noinspection PyUnresolvedReferences
        wyczysc_btn.clicked.connect(self.wyczysc_polaczenia)
        controls.addWidget(wyczysc_btn)

        generuj_btn = QPushButton("Generuj 5 losowych miast")
        # noinspection PyUnresolvedReferences
        generuj_btn.clicked.connect(self.generuj_losowe_miasta)
        controls.addWidget(generuj_btn)

        znajdz_btn = QPushButton("Znajdź optymalną trasę")
        # noinspection PyUnresolvedReferences
        znajdz_btn.clicked.connect(self.znajdz_najlepsza_trase)
        controls.addWidget(znajdz_btn)

        eksport_miasta_btn = QPushButton("Eksportuj miasta do pliku")
        # noinspection PyUnresolvedReferences
        eksport_miasta_btn.clicked.connect(self.eksportuj_miasta)
        controls.addWidget(eksport_miasta_btn)

        eksport_drogi_btn = QPushButton("Eksportuj drogi do pliku")
        # noinspection PyUnresolvedReferences
        eksport_drogi_btn.clicked.connect(self.eksportuj_drogi)
        controls.addWidget(eksport_drogi_btn)

        wczytaj_miasta_btn = QPushButton("Wczytaj miasta z pliku")
        # noinspection PyUnresolvedReferences
        wczytaj_miasta_btn.clicked.connect(self.wczytaj_miasta)
        controls.addWidget(wczytaj_miasta_btn)

        wczytaj_drogi_btn = QPushButton("Wczytaj drogi z pliku")
        # noinspection PyUnresolvedReferences
        wczytaj_drogi_btn.clicked.connect(self.wczytaj_drogi)
        controls.addWidget(wczytaj_drogi_btn)

        layout.addLayout(controls)
        layout.addWidget(self.canvas)
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


    def eksportuj_miasta(self):
        try:
            with open("miasta.txt", "w") as f:
                for nazwa, (x, y) in self.miasta.items():
                    f.write(f"{nazwa},{x},{y}\n")
        except Exception as e:
            QMessageBox.critical(self, "Błąd", f"Nie udało się zapisać miast:\n{str(e)}")


    def eksportuj_drogi(self):
        try:
            with open("drogi.txt", "w") as f:
                for m1, m2 in self.drogi:
                    f.write(f"{m1},{m2}\n")
        except Exception as e:
            QMessageBox.critical(self, "Błąd", f"Nie udało się zapisać dróg:\n{str(e)}")


    def wczytaj_miasta(self):
        try:
            with open("miasta.txt", "r") as f:
                self.miasta.clear()
                for line in f:
                    parts = line.strip().split(",")
                    if len(parts) == 3:
                        nazwa, x, y = parts
                        self.miasta[nazwa] = (float(x), float(y))
            self.drogi.clear()
            self.rysuj_mape()
        except Exception as e:
            QMessageBox.critical(self, "Błąd", f"Nie udało się wczytać miast:\n{str(e)}")


    def wczytaj_drogi(self):
        try:
            with open("drogi.txt", "r") as f:
                self.drogi.clear()
                for line in f:
                    m1, m2 = line.strip().split(",")
                    if m1 in self.miasta and m2 in self.miasta:
                        self.drogi.append((m1, m2))
            self.rysuj_mape()
        except Exception as e:
            QMessageBox.critical(self, "Błąd", f"Nie udało się wczytać dróg:\n{str(e)}")


    def dystans(self, trasa):
        dyst = 0
        for i in range(len(trasa)):
            m1 = trasa[i]
            m2 = trasa[(i + 1) % len(trasa)]
            x1, y1 = self.miasta[m1]
            x2, y2 = self.miasta[m2]
            dyst += math.hypot(x2 - x1, y2 - y1)
        return dyst


    @staticmethod
    def krzyzowanie(p1, p2):
        a, b = sorted(random.sample(range(len(p1)), 2))
        srodek = p1[a:b]
        pozostale = [m for m in p2 if m not in srodek]
        return pozostale[:a] + srodek + pozostale[a:]


    @staticmethod
    def mutacja(trasa, wsp=0.1):
        for i in range(len(trasa)):
            if random.random() < wsp:
                j = random.randint(0, len(trasa) - 1)
                trasa[i], trasa[j] = trasa[j], trasa[i]


    def znajdz_najlepsza_trase(self, pokolenia=500, populacja_rozmiar=200):
        miasta_lista = list(self.miasta.keys())
        if len(miasta_lista) < 2:
            QMessageBox.warning(self, "Uwaga", "Potrzebujesz co najmniej 2 miast")
            return

        populacja = [random.sample(miasta_lista, len(miasta_lista)) for _ in range(populacja_rozmiar)]

        najlepszy_dystans = float('inf')
        stagnacja_licznik = 0
        max_stagnacja = 50

        for epoka in range(pokolenia):
            populacja.sort(key=lambda trasa: self.dystans(trasa))
            nowa_populacja = populacja[:10]

            obecny_dystans = self.dystans(nowa_populacja[0])

            if abs(najlepszy_dystans - obecny_dystans) < 0.1:
                stagnacja_licznik += 1
            else:
                stagnacja_licznik = 0
                najlepszy_dystans = obecny_dystans

            if stagnacja_licznik >= max_stagnacja:
                print(f"Zakończono po {epoka + 1} pokoleniach z powodu stabilności rozwiązania")
                break

            while len(nowa_populacja) < populacja_rozmiar:
                rodzic1, rodzic2 = random.sample(populacja[:20], 2)
                dziecko = self.krzyzowanie(rodzic1, rodzic2)
                self.mutacja(dziecko)
                nowa_populacja.append(dziecko)

            populacja = nowa_populacja

        najlepsza = min(populacja, key=self.dystans)
        self.rysuj_mape(najlepsza)


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


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = KomiwojazerApp()
    window.resize(1000, 600)
    window.show()
    sys.exit(app.exec_())
