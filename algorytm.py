import math
import random
from PyQt5.QtWidgets import QMessageBox


def zapisz_trase_od_podanej_nazwy(self, start: str) -> None:
    if not self.najlepsza_trasa or start not in self.najlepsza_trasa:
        QMessageBox.warning(self, "Uwaga", "Trasa jest pusta lub nie zawiera podanego miasta")
        return

    idx = self.najlepsza_trasa.index(start)
    obrocona_trasa = self.najlepsza_trasa[idx:] + self.najlepsza_trasa[:idx]
    calkowita_odleglosc = dystans(self.miasta, obrocona_trasa)
    trasa_jako_tekst = " -> ".join(obrocona_trasa)
    linijka_do_pliku = f"{trasa_jako_tekst}\nSuma odległości: {calkowita_odleglosc:.2f}\n\n"

    try:
        with open("wybrane.txt", "w") as file:
            file.write(linijka_do_pliku)
    except Exception as e:
        QMessageBox.critical(self, "Błąd zapisu", f"Nie udało się zapisać trasy: {str(e)}")
        return

    QMessageBox.information(self, "Wybrana trasa", linijka_do_pliku)


def zapisz_najlepsza_trase_do_pliku(self) -> None:
    calkowita_odleglosc: float = dystans(self.miasta, self.najlepsza_trasa)
    trasa_jako_tekst: str = " -> ".join(self.najlepsza_trasa)
    linijka_do_pliku: str = f"{trasa_jako_tekst}\nSuma odległości: {calkowita_odleglosc:.2f}\n\n"

    try:
        with open("najlepsze_trasy.txt", "a") as file:
            file.write(linijka_do_pliku)
    except Exception as e:
        QMessageBox.critical(self, "Błąd zapisu", f"Nie udało się zapisać trasy: {str(e)}")
        return


def dystans(miasta: dict[str, tuple[float, float]], trasa: list[str]) -> float:
    dyst: float = 0.0
    for i in range(len(trasa)):
        miasto1: str = trasa[i]
        miasto2: str = trasa[(i + 1) % len(trasa)]
        x1, y1 = miasta[miasto1]
        x2, y2 = miasta[miasto2]
        dyst += math.hypot(x2 - x1, y2 - y1)
    return dyst


def krzyzowanie(p1: list[str], p2: list[str]) -> list[str]:
    a, b = sorted(random.sample(range(len(p1)), 2))
    srodek: list[str] = p1[a:b]
    pozostale: list[str] = [m for m in p2 if m not in srodek]
    return pozostale[:a] + srodek + pozostale[a:]


def mutacja(trasa: list[str], wsp: float = 0.1) -> None:
    for i in range(len(trasa)):
        if random.random() < wsp:
            j: int = random.randint(0, len(trasa) - 1)
            trasa[i], trasa[j] = trasa[j], trasa[i]


def znajdz_najlepsza_trase_genetyczny(self, pokolenia: int = 500, populacja_rozmiar: int = 200) -> None:
    miasta_lista: list[str] = list(self.miasta.keys())
    if len(miasta_lista) < 2:
        QMessageBox.warning(self, "Uwaga", "Potrzebujesz co najmniej 2 miast")
        return

    populacja: list[list[str]] = [random.sample(miasta_lista, len(miasta_lista)) for _ in range(populacja_rozmiar)]

    najlepszy_dystans: float = float("inf")
    stagnacja_licznik: int = 0
    max_stagnacja: int = 50

    for epoka in range(pokolenia):
        populacja.sort(key=lambda trasa: dystans(self.miasta, trasa))
        nowa_populacja: list[list[str]] = populacja[:10]

        obecny_dystans: float = dystans(self.miasta, nowa_populacja[0])

        if (abs(najlepszy_dystans - obecny_dystans)) / obecny_dystans < 0.001:
            stagnacja_licznik += 1
        else:
            stagnacja_licznik = 0
            najlepszy_dystans = obecny_dystans

        if stagnacja_licznik >= max_stagnacja:
            break

        while len(nowa_populacja) < populacja_rozmiar:
            rodzic1, rodzic2 = random.sample(populacja[:20], 2)
            dziecko: list[str] = krzyzowanie(rodzic1, rodzic2)
            mutacja(dziecko)
            nowa_populacja.append(dziecko)

        populacja = nowa_populacja

    self.najlepsza_trasa = min(populacja, key=lambda trasa: dystans(self.miasta, trasa))

    self.rysuj_mape()

    zapisz_najlepsza_trase_do_pliku(self)


def znajdz_najlepsza_trase_najblizszego_sasiada(self) -> None:
    miasta: dict[str, tuple[float, float]] = self.miasta

    if len(miasta) < 2:
        QMessageBox.warning(self, "Uwaga", "Potrzebujesz co najmniej 2 miast")
        return

    nazwy: list[str] = list(miasta.keys())


    def najblizszy_sasiad(start: str) -> list[str]:
        nieodwiedzone: set[str] = set(nazwy)
        trasa: list[str] = [start]
        nieodwiedzone.remove(start)
        while nieodwiedzone:
            ostatnie: str = trasa[-1]
            najblizsze: str = min(
                nieodwiedzone,
                key=lambda m: math.hypot(
                    miasta[ostatnie][0] - miasta[m][0],
                    miasta[ostatnie][1] - miasta[m][1]
                )
            )
            trasa.append(najblizsze)
            nieodwiedzone.remove(najblizsze)
        return trasa


    najlepsza_trasa: list[str] = []
    najlepszy_dystans: float = float("inf")
    for start in nazwy:
        trasa: list[str] = najblizszy_sasiad(start)
        dist: float = dystans(miasta, trasa)
        if dist < najlepszy_dystans:
            najlepszy_dystans = dist
            najlepsza_trasa = trasa

    self.najlepsza_trasa = najlepsza_trasa

    self.rysuj_mape()

    zapisz_najlepsza_trase_do_pliku(self)
