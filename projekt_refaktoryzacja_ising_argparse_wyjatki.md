# Projekt - refaktoryzacja symulacji modelu Isinga, moduły, `argparse` i obsługa wyjątków

## Cel zadania

Celem zadania jest rozwinięcie wcześniejszej implementacji symulacji Monte Carlo modelu Isinga. Tym razem nacisk ma być położony nie tylko na samą symulację, ale również na organizację kodu, uruchamianie programu z linii poleceń oraz poprawną obsługę błędów.

Punktem wyjścia jest wcześniejsze rozwiązanie, w którym symulacja była przygotowana w notebooku. Należy je teraz uporządkować i przenieść do klasycznej struktury projektu w Pythonie.

## Ogólny opis zadania

Należy przebudować dotychczasowy kod tak, aby:

1. fragmenty odpowiedzialne za właściwą symulację, w szczególności te wykorzystujące Numba, zostały przeniesione do osobnego modułu w pliku `*.py`,
2. uruchamianie symulacji odbywało się nie z notebooka, lecz z osobnego skryptu `*.py`,
3. parametry symulacji były pobierane z linii poleceń za pomocą modułu `argparse`,
4. program potrafił reagować na błędne dane wejściowe poprzez zgłaszanie i obsługę wyjątków,
5. użytkownik mógł opcjonalnie:
   - zapisać magnetyzację do pliku,
   - wyświetlić animację,
   - zapisać animację do pliku.

## Część 1 - wydzielenie kodu do osobnego modułu

Kod odpowiedzialny za właściwą symulację należy przenieść z notebooka do osobnego pliku `*.py`.

Minimalnym wymaganiem jest utworzenie osobnego modułu, na przykład:

```text
ising_numba.py
```

w którym znajdą się funkcje związane z symulacją, na przykład:

- inicjalizacja siatki spinów,
- obliczanie zmiany energii,
- wykonanie jednego makrokroku,
- wykonanie całej symulacji,
- obliczanie magnetyzacji,
- ewentualnie funkcje pomocnicze.

Główny skrypt uruchamiający program ma te elementy importować, zamiast definiować je lokalnie.

Osoby ambitniejsze mogą przygotować prosty pakiet, czyli katalog z plikiem `__init__.py` i podziałem kodu na kilka modułów, na przykład osobno dla:

- symulacji,
- wizualizacji,
- obsługi argumentów,
- funkcji pomocniczych.

Nie jest to jednak wymagane. Wystarczy poprawnie działający pojedynczy moduł.

## Część 2 - uruchamianie symulacji ze skryptu

Właściwe wykonanie symulacji ma zostać przeniesione z notebooka do skryptu `*.py`.

Notebook może ewentualnie służyć później do testów lub analizy wyników, ale główna wersja programu powinna być uruchamiana z terminala, na przykład w stylu:

```bash
python run_ising.py --N 100 --M 500 --beta 0.6 --B 0.0 --J 1.0 --show-animation
```

To właśnie skrypt uruchamiający powinien:

- pobrać argumenty z linii poleceń,
- sprawdzić ich poprawność,
- uruchomić symulację,
- ewentualnie zapisać wyniki do plików,
- ewentualnie wyświetlić animację,
- przechwycić i obsłużyć błędy.

## Część 3 - użycie `argparse`

Skrypt uruchamiający ma wykorzystywać moduł `argparse` do pobierania parametrów symulacji z linii poleceń.

### Wymagane argumenty lub parametry z wartościami domyślnymi

Program ma umożliwiać podanie następujących parametrów symulacji:

- rozmiar siatki $N$,
- liczba makrokroków $M$,
- parametr $\beta$,
- wartość pola zewnętrznego $B$,
- wartość stałej oddziaływania $J$.

Dla tych parametrów należy ustawić sensowne wartości domyślne, tak aby program dało się uruchomić również bez podawania wszystkich opcji ręcznie.

Przykładowo można przyjąć takie domyślne wartości:

- $N = 100$
- $M = 500$
- $\beta = 0.4$
- $B = 0.0$
- $J = 1.0$

Można też dobrać inne rozsądne wartości, o ile zostaną jasno opisane w programie lub w komentarzu.

### Parametr opcjonalny - zapis magnetyzacji

Należy dodać opcjonalny parametr pozwalający podać nazwę pliku, do którego zostanie zapisana magnetyzacja w funkcji czasu.

Jeżeli taki parametr nie zostanie podany, magnetyzacja nie powinna być zapisywana do pliku.

Można to zrealizować na przykład przez opcję w rodzaju:

```bash
--magnetization-file magnetization.txt
```

lub

```bash
--magnetization-file magnetization.csv
```

Format pliku można dobrać samodzielnie. Najprostsza wersja to zapis numeru kroku i wartości magnetyzacji w kolejnych wierszach.

### Flaga - wyświetlanie animacji

Należy dodać flagę określającą, czy po zakończeniu symulacji ma zostać wyświetlone okno z animacją.

Jeżeli flaga nie zostanie podana, program nie powinien otwierać okna z animacją.

Przykładowa flaga:

```bash
--show-animation
```

### Parametr opcjonalny - zapis animacji

Opcjonalnie można dodać parametr pozwalający zapisać animację do pliku, na przykład:

```bash
--animation-file ising.mp4
```

albo

```bash
--animation-file ising.gif
```

To rozszerzenie nie jest obowiązkowe, ale jest mile widziane.

## Część 4 - obsługa wyjątków

Do programu należy wprowadzić obsługę błędów opartą na wyjątkach.

Chodzi o to, aby program nie kończył się chaotycznie przy błędnych danych, lecz:

1. wykrywał problem,
2. zgłaszał odpowiedni wyjątek,
3. przechwytywał go w kontrolowany sposób,
4. wypisywał użytkownikowi czytelny komunikat.

### Przykład obowiązkowy

Jeżeli użytkownik poda ujemną wartość $\beta$, program powinien zgłosić wyjątek.

W tym przypadku naturalnym wyborem jest wbudowany wyjątek:

```python
ValueError
```

ponieważ problem dotyczy niepoprawnej wartości argumentu.

### Inne sytuacje, w których warto zgłaszać wyjątki

Warto rozważyć także inne przypadki, w których program powinien zgłaszać wyjątek, na przykład:

- $N \leq 0$ - rozmiar siatki musi być dodatni,
- $M \leq 0$ - liczba makrokroków musi być dodatnia,
- podanie niepoprawnej nazwy pliku lub problem z zapisem do pliku,
- próba zapisania animacji do formatu, którego nie da się obsłużyć w danym środowisku,
- przekazanie argumentu o nieprawidłowym typie lub wartości.

W zależności od sytuacji można wykorzystać odpowiednie wbudowane wyjątki, na przykład:

- `ValueError` - gdy wartość parametru jest niepoprawna,
- `TypeError` - gdy obiekt ma niewłaściwy typ,
- `OSError` lub jego podtypy, na przykład `FileNotFoundError`, gdy problem dotyczy plików lub systemu plików,
- `RuntimeError` - gdy wystąpi błąd wykonania, którego nie da się sensownie zakwalifikować bardziej szczegółowo.

Nie trzeba sztucznie generować wyjątków wszędzie. Chodzi o miejsca, w których rzeczywiście ma to sens i poprawia jakość programu.

## Część 5 - obsługa wyjątków w skrypcie głównym

Sam moduł z symulacją może zgłaszać wyjątki, ale główny skrypt powinien je również obsługiwać.

To oznacza, że w skrypcie uruchamiającym należy zastosować konstrukcję `try` / `except`, tak aby w razie błędu:

- wypisać czytelny komunikat,
- zakończyć program w kontrolowany sposób,
- ewentualnie zwrócić odpowiedni kod wyjścia.

Nie należy zostawiać użytkownika z nieczytelnym komunikatem lub przypadkowym zawieszeniem programu.


## Oczekiwana struktura programu

Minimalna sensowna struktura może wyglądać na przykład tak:

```text
project/
├── ising_numba.py
└── run_ising.py
```

gdzie:

- `ising_numba.py` zawiera logikę symulacji,
- `run_ising.py` zawiera kod uruchamiany z terminala, `argparse`, obsługę wyjątków i wywołanie funkcji z modułu.

Bardziej rozbudowana wersja może wyglądać tak:

```text
project/
├── ising/
│   ├── __init__.py
│   ├── simulation.py
│   ├── visualization.py
│   └── io_utils.py
└── run_ising.py
```

Taki podział nie jest obowiązkowy, ale jest bardzo dobrym ćwiczeniem.


## Przykładowe uruchomienia

### Uruchomienie z wartościami domyślnymi

```bash
python run_ising.py
```

### Uruchomienie z własnymi parametrami

```bash
python run_ising.py --N 120 --M 1000 --beta 0.55 --B 0.1 --J 1.0
```

### Uruchomienie z zapisem magnetyzacji

```bash
python run_ising.py --N 120 --M 1000 --beta 0.55 --B 0.1 --J 1.0 --magnetization-file magnetization.csv
```

### Uruchomienie z wyświetleniem animacji

```bash
python run_ising.py --show-animation
```

### Uruchomienie z zapisem animacji

```bash
python run_ising.py --show-animation --animation-file ising.mp4
```

## Wymagania końcowe

Należy oddać program, który:

1. przenosi logikę symulacji do osobnego modułu lub pakietu,
2. uruchamia symulację z pliku `*.py`, a nie bezpośrednio z notebooka,
3. pobiera parametry z linii poleceń przy pomocy `argparse`,
4. posiada wartości domyślne dla podstawowych parametrów,
5. umożliwia opcjonalny zapis magnetyzacji do pliku,
6. posiada flagę włączającą wyświetlanie animacji,
7. opcjonalnie pozwala zapisać animację do pliku,
8. wykorzystuje wyjątki do obsługi błędnych danych i problemów wykonania,
9. przechwytuje te wyjątki w skrypcie głównym i wypisuje czytelne komunikaty.

## Na co zwrócić uwagę

Najważniejsze w tym zadaniu są trzy rzeczy:

- sensowny podział kodu na moduły,
- poprawne użycie `argparse`,
- obsługa błędów za pomocą wyjątków.

Chodzi o to, aby program nie był już tylko jednorazowym kodem z notebooka, ale przypominał małą, uporządkowaną aplikację uruchamianą z terminala.

Powodzenia.
