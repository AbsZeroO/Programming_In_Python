# Symulacja Polowania Wilka na Owce - Instrukcja Implementacji

## Opis Zadania

Celem jest stworzenie symulacji, w której wilk próbuje złapać owce porozrzucane na nieskończonej łące. Symulacja odbywa się w trybie tekstowym, a teren jest reprezentowany jako dwuwymiarowa przestrzeń kartezjańska. Wilk goni owce, które poruszają się losowo, a po złapaniu owca znika z łąki.

---

## Wymagania Funkcjonalne

1. **Inicjalizacja symulacji**:
   - Wilk zaczyna w punkcie centralnym łąki (0.0, 0.0).
   - Pozycje owiec są losowane w zakresie od -10.0 do 10.0 dla każdej współrzędnej.
   - Domyślne wartości:
     - Maksymalna liczba rund: 50
     - Liczba owiec: 15
     - Odległość ruchu owcy: 0.5
     - Odległość ruchu wilka: 1.0

2. **Ruch zwierząt**:
   - **Owce**: Każda owca w każdej rundzie losowo wybiera kierunek (północ, południe, wschód, zachód) i przemieszcza się o określoną odległość.
   - **Wilk**: Wilk identyfikuje najbliższą owcę. Jeśli owca jest w zasięgu ataku, wilk ją zjada i zajmuje jej miejsce. W przeciwnym razie wilk porusza się w jej stronę.

3. **Zakończenie symulacji**:
   - Symulacja kończy się, gdy wszystkie owce zostaną zjedzone lub gdy osiągnięta zostanie maksymalna liczba rund.

4. **Wyświetlanie informacji po rundach**:
   - Po każdej rundzie wyświetlane są informacje:
     - Numer rundy.
     - Pozycja wilka (z dokładnością do trzech miejsc po przecinku).
     - Liczba żywych owiec.
     - Jeśli wilk ściga owcę - numer tej owcy.
     - Jeśli owca została zjedzona - numer tej owcy.

---

## Zapisywanie Wyników

1. **Zapis pozycji do pliku JSON**:
   - Każda runda kończy się zapisem pozycji zwierząt do `pos.json`.
   - Struktura pliku:
     - `round_no` - numer rundy.
     - `wolf_pos` - pozycja wilka.
     - `sheep_pos` - lista pozycji owiec lub wartość `null` dla zjedzonych owiec.
   - Format pliku ma być czytelny i sformatowany. Jeśli `pos.json` istnieje, zostaje nadpisany.

2. **Zapis liczby żywych owiec do pliku CSV**:
   - Po każdej rundzie liczba żywych owiec jest zapisywana do `alive.csv`.
   - Struktura pliku:
     - Kolumna 1: numer rundy.
     - Kolumna 2: liczba żywych owiec.
   - Jeśli `alive.csv` istnieje, zostaje nadpisany.

---

## Implementacja Argumentów Wiersza Poleceń

1. Użyj modułu `argparse` do obsługi opcjonalnych argumentów:
   - `-c/--config FILE`: plik konfiguracyjny z wartościami pozycji początkowych i odległości ruchu.
   - `-h/--help`: wyświetla wiadomość pomocniczą i kończy działanie programu.
   - `-l/--log LEVEL`: zapis zdarzeń do logu na określonym poziomie (DEBUG, INFO, WARNING, ERROR, CRITICAL).
   - `-r/--rounds NUM`: maksymalna liczba rund (domyślnie 50).
   - `-s/--sheep NUM`: liczba owiec (domyślnie 15).
   - `-w/--wait`: wstrzymanie symulacji po każdej rundzie do naciśnięcia klawisza.

2. **Walidacja argumentów**:
   - Parametry muszą być poprawnie sformatowane, np. liczba rund musi być dodatnią liczbą całkowitą.

---

## Konfiguracja Pliku

1. **Plik INI** z parametrami symulacji:
   - Użyj modułu `configparser` do wczytywania wartości z pliku, którego nazwa jest podana w `-c/--config`.
   - Struktura pliku INI:
     ```ini
     [Sheep]
     InitPosLimit = 10.0
     MoveDist = 0.5

     [Wolf]
     MoveDist = 1.0
     ```
2. **Walidacja wartości**: Sprawdź, czy parametry są poprawne, np. odległość ruchu wilka musi być dodatnia.

---

## Logowanie Zdarzeń

1. **Plik logu** `chase.log`:
   - Użyj modułu `logging` do zapisu zdarzeń w oparciu o poziom szczegółowości wybrany przez `-l/--log`.
   - Poziomy logowania:
     - **DEBUG**: Szczegóły techniczne (np. kierunek ruchu każdej owcy, odległości do owiec).
     - **INFO**: Ogólne informacje (np. początek nowej rundy, liczba żywych owiec na końcu rundy).
     - **WARNING**: Ostrzeżenia.
     - **ERROR**: Błędy.
     - **CRITICAL**: Krytyczne błędy.
2. **Przykładowe zdarzenia do logowania**:
   - Pozycje początkowe zwierząt, ruch każdego zwierzęcia, liczba żywych owiec po rundzie, zakończenie symulacji.

---

## Obsługa Błędów

1. **Walidacja parametrów**:
   - Sprawdzaj poprawność danych wejściowych i podanych argumentów.
   - Generuj wyjątki w przypadku błędnych wartości.
2. **Brak logowania błędów z argumentami**:
   - Błędy związane z argumentami wiersza poleceń nie muszą być zapisywane w logu.
