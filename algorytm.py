
import math
import random
from PyQt5.QtWidgets import QMessageBox


def dystans(miasta, trasa):
    dyst = 0
    for i in range(len(trasa)):
        m1 = trasa[i]
        m2 = trasa[(i + 1) % len(trasa)]
        x1, y1 = miasta[m1]
        x2, y2 = miasta[m2]
        dyst += math.hypot(x2 - x1, y2 - y1)
    return dyst


def krzyzowanie(p1, p2):
    a, b = sorted(random.sample(range(len(p1)), 2))
    srodek = p1[a:b]
    pozostale = [m for m in p2 if m not in srodek]
    return pozostale[:a] + srodek + pozostale[a:]


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
        populacja.sort(key=lambda trasa: dystans(self.miasta, trasa))
        nowa_populacja = populacja[:10]

        obecny_dystans = dystans(self.miasta, nowa_populacja[0])

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
            dziecko = krzyzowanie(rodzic1, rodzic2)
            mutacja(dziecko)
            nowa_populacja.append(dziecko)

        populacja = nowa_populacja

    najlepsza = min(populacja, key=lambda trasa: dystans(self.miasta, trasa))
    self.rysuj_mape(najlepsza)
