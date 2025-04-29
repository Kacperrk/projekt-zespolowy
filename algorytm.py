import math
import random
from typing import List, Dict, Tuple, Any
from PyQt5.QtWidgets import QMessageBox


def zapisz_najlepsza_trase_do_pliku(self: Any, najlepsza: List[str]) -> None:
    calkowita_odleglosc: float = dystans(self.miasta, najlepsza)
    trasa_jako_tekst: str = " -> ".join(najlepsza)
    linijka_do_pliku: str = f"{trasa_jako_tekst}\nSuma odległości: {calkowita_odleglosc:.2f}\n\n"

    try:
        # Przy zmianie najlepsze_trasy.txt zmienić też w .gitignore
        with open("najlepsze_trasy.txt", "a") as file:
            file.write(linijka_do_pliku)
    except Exception as e:
        QMessageBox.critical(self, "Błąd zapisu", f"Nie udało się zapisać trasy: {str(e)}")


def dystans(miasta: Dict[str, Tuple[float, float]], trasa: List[str]) -> float:
    dyst: float = 0.0
    for i in range(len(trasa)):
        m1: str = trasa[i]
        m2: str = trasa[(i + 1) % len(trasa)]
        x1, y1 = miasta[m1]
        x2, y2 = miasta[m2]
        dyst += math.hypot(x2 - x1, y2 - y1)
    return dyst


def krzyzowanie(p1: List[str], p2: List[str]) -> List[str]:
    a, b = sorted(random.sample(range(len(p1)), 2))
    srodek: List[str] = p1[a:b]
    pozostale: List[str] = [m for m in p2 if m not in srodek]
    return pozostale[:a] + srodek + pozostale[a:]


def mutacja(trasa: List[str], wsp: float = 0.1) -> None:
    for i in range(len(trasa)):
        if random.random() < wsp:
            j: int = random.randint(0, len(trasa) - 1)
            trasa[i], trasa[j] = trasa[j], trasa[i]


def znajdz_najlepsza_trase_genetyczny(self: Any, pokolenia: int = 500, populacja_rozmiar: int = 200) -> None:
    miasta_lista: List[str] = list(self.miasta.keys())
    if len(miasta_lista) < 2:
        QMessageBox.warning(self, "Uwaga", "Potrzebujesz co najmniej 2 miast")
        return

    populacja: List[List[str]] = [random.sample(miasta_lista, len(miasta_lista)) for _ in range(populacja_rozmiar)]

    najlepszy_dystans: float = float('inf')
    stagnacja_licznik: int = 0
    max_stagnacja: int = 50

    for epoka in range(pokolenia):
        populacja.sort(key=lambda trasa: dystans(self.miasta, trasa))
        nowa_populacja: List[List[str]] = populacja[:10]

        obecny_dystans: float = dystans(self.miasta, nowa_populacja[0])

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
            dziecko: List[str] = krzyzowanie(rodzic1, rodzic2)
            mutacja(dziecko)
            nowa_populacja.append(dziecko)

        populacja = nowa_populacja

    najlepsza: List[str] = min(populacja, key=lambda trasa: dystans(self.miasta, trasa))
    self.rysuj_mape(najlepsza)
    zapisz_najlepsza_trase_do_pliku(self, najlepsza)


def znajdz_najlepsza_trase_najblizszego_sasiada(self: Any) -> None:
    miasta: Dict[str, Tuple[float, float]] = self.miasta

    if len(miasta) < 2:
        QMessageBox.warning(self, "Uwaga", "Potrzebujesz co najmniej 2 miast")
        return

    nazwy: List[str] = list(miasta.keys())

    def najblizszy_sasiad(start: str) -> List[str]:
        nieodwiedzone: set[str] = set(nazwy)
        trasa: List[str] = [start]
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

    najlepsza_trasa: List[str] = []
    najlepszy_dystans: float = float('inf')
    for start in nazwy:
        trasa: List[str] = najblizszy_sasiad(start)
        dist: float = dystans(miasta, trasa)
        if dist < najlepszy_dystans:
            najlepszy_dystans = dist
            najlepsza_trasa = trasa

    self.rysuj_mape(najlepsza_trasa)
    zapisz_najlepsza_trase_do_pliku(self, najlepsza_trasa)
