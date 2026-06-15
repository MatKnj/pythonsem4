# Zadania - Dekoratory i Generatory

## Zadanie 1 - Dekorator mierzący czas wykonania funkcji

### Cel zadania

Celem zadania jest przećwiczenie tworzenia **dekoratorów zaimplementowanych w postaci obiektów**. Zadanie ma również pokazać, jak można gromadzić informacje o wywołaniach funkcji i później je analizować.

Waszym zadaniem jest napisanie dekoratora, który:

- mierzy czas wykonania dekorowanej funkcji,
- zapamiętuje informacje o kolejnych wywołaniach,
- potrafi - na życzenie - wyświetlić statystyki dotyczące zebranych pomiarów.

### Treść zadania

Należy zaimplementować klasę pełniącą rolę dekoratora, na przykład `TimerDecorator` (nazwa klasy może być inna, ale powinna jasno opisywać jej przeznaczenie).

Dekorator powinien działać w następujący sposób:

1. Po udekorowaniu funkcji każde jej wywołanie ma zostać zmierzone czasowo.
2. Dla każdej dekorowanej funkcji należy przechowywać historię pomiarów.
3. Dekorator ma umożliwiać wypisanie statystyk dla danej funkcji.
4. Implementacja dekoratora ma być **obiektowa**, to znaczy nie chodzi tutaj o zwykłą funkcję zwracającą funkcję, ale o klasę z odpowiednio zaimplementowanym mechanizmem wywołania.

### Wymagania podstawowe

Wasze rozwiązanie powinno spełniać następujące warunki:

#### 1. Implementacja dekoratora jako obiektu

Dekorator ma być klasą. Oznacza to, że należy wykorzystać mechanizm `__call__`, tak aby możliwe było użycie go składnią:

```python
@TimerDecorator
def moja_funkcja(...):
    ...
```

albo - jeśli ktoś woli nieco inną koncepcję - inną równoważną postacią opartą na obiekcie.

#### 2. Pomiar czasu wykonania

Do pomiaru czasu należy użyć mechanizmu o odpowiedniej dokładności, np. `time.perf_counter()`.

Pomiar powinien obejmować rzeczywisty czas wykonania funkcji - od momentu wejścia do funkcji do momentu jej zakończenia.

#### 3. Zapamiętywanie historii wywołań

Dla każdej dekorowanej funkcji należy zapamiętywać co najmniej:

- liczbę wywołań,
- czasy kolejnych wykonań.

Możecie przechowywać dodatkowe informacje, jeśli uznacie to za sensowne.

#### 4. Statystyki

Dekorator ma umożliwiać wyświetlenie statystyk dla danej funkcji. Statystyki powinny zawierać co najmniej:

- nazwę funkcji,
- liczbę wywołań,
- najkrótszy czas wykonania,
- najdłuższy czas wykonania,
- średni czas wykonania.

Forma prezentacji jest dowolna, ale wynik powinien być czytelny.

### Wymagania dodatkowe

Do podstawowej wersji zadania należy dodać przynajmniej **dwa** z poniższych rozszerzeń:

#### Wariant A - możliwość włączania i wyłączania wypisywania czasu przy każdym wywołaniu

Dekorator może przyjmować parametr, który decyduje, czy po każdym wywołaniu funkcji ma zostać wypisana informacja o czasie wykonania.

Przykład idei:

```python
@TimerDecorator(print_each_call=True)
def obliczenia(...):
    ...
```

#### Wariant B - ograniczenie liczby przechowywanych pomiarów

Dekorator może przyjmować parametr określający maksymalną liczbę ostatnich pomiarów, które są przechowywane. Po przekroczeniu tego limitu najstarsze wyniki powinny być usuwane.

#### Wariant C - osobna metoda do pobierania statystyk

Zamiast ograniczać się do wypisywania statystyk na ekran, można przygotować metodę zwracającą statystyki w postaci słownika lub obiektu, który da się dalej wykorzystać w programie.

#### Wariant D - zachowanie metadanych funkcji

Warto zadbać o to, aby po dekoracji funkcja zachowała swoją nazwę i dokumentację. Można to zrobić np. przy użyciu `@functools.wraps` albo podobnego mechanizmu (przeczytajcie w dokumentacji `@functools.wraps` co robi ten dekorator i po co jest potrzebny).

### Wskazówki projektowe

Dobrym pomysłem jest też wydzielenie metod pomocniczych, np.:

- metody odpowiedzialnej za wypisywanie statystyk,
- metody zwracającej surowe dane pomiarowe,
- metody resetującej zebrane statystyki.

### Minimalny przykład użycia

Wasz program powinien zawierać demonstrację działania dekoratora na co najmniej **dwóch różnych funkcjach**.

Przykładowo mogą to być:

- funkcja wykonująca sztucznie opóźnione działanie,
- funkcja obliczeniowa.

Nie chodzi o złożoność tych funkcji, ale o sensowne pokazanie, że dekorator rzeczywiście działa.

### Czego oczekuję w rozwiązaniu

Rozwiązanie powinno zawierać:

1. implementację dekoratora jako klasy,
2. kod testujący działanie dekoratora,
3. prezentację statystyk dla dekorowanych funkcji.

### Na co warto uważać

Zwróćcie uwagę między innymi na następujące kwestie:

- poprawne przekazywanie argumentów `*args` i `**kwargs` do dekorowanej funkcji,
- poprawne zwracanie wyniku dekorowanej funkcji,
- czytelność interfejsu dekoratora,
- sensowny podział odpowiedzialności między metody klasy.


### Dla chętnych

Osoby, które chcą zrobić coś więcej, mogą spróbować jednego z poniższych rozszerzeń:

- umożliwić zapis statystyk do pliku,
- przygotować dekorator tak, aby dało się go używać zarówno z argumentami, jak i bez argumentów.

### Uwagi techniczne

- Nie używamy gotowych bibliotek do profilowania.
- Chodzi o samodzielną implementację mechanizmu dekoratora.
- Kod powinien być napisany w sposób możliwie przejrzysty i zgodny z dobrymi praktykami Pythona.

---

## Zadanie 2 - klasa `Temperature` i właściwości `@property`

### Cel zadania

Celem zadania jest przećwiczenie użycia mechanizmu `@property`, a więc tworzenia **atrybutów**, które z punktu widzenia użytkownika klasy wyglądają jak zwykłe atrybuty, ale w rzeczywistości mogą wykonywać dodatkowe obliczenia i kontrolować poprawność przypisywanych wartości.

W tym zadaniu należy napisać klasę reprezentującą temperaturę oraz zadbać o to, aby można było wygodnie odczytywać i ustawiać jej wartość w różnych skalach.

### Treść zadania

Należy zaimplementować klasę `Temperature`, która **wewnętrznie przechowuje temperaturę w stopniach Celsjusza**, ale udostępnia użytkownikowi interfejs pozwalający pracować również ze skalą Fahrenheita i Kelvina.

Klasa ma wykorzystywać `@property`.

### Wymagania podstawowe

#### 1. Konstruktor

Klasa powinna umożliwiać utworzenie obiektu z temperaturą początkową podaną w stopniach Celsjusza, na przykład:

```python
t = Temperature(25)
```

#### 2. Wewnętrzne przechowywanie danych

Temperatura ma być przechowywana wewnętrznie w prywatnym polu, np.:

```python
self._celsius
```

Nie należy przechowywać osobno temperatury w kelwinach i fahrenheitach. Te wartości mają być obliczane na podstawie jednej wartości wewnętrznej.

#### 3. Atrybut `celsius`

Klasa ma udostępniać atrybut `celsius`, który pozwala:

- odczytać temperaturę w stopniach Celsjusza,
- ustawić temperaturę w stopniach Celsjusza.

#### 4. Atrybut `fahrenheit`

Klasa ma udostępniać atrybut `fahrenheit`, który pozwala:

- odczytać temperaturę w stopniach Fahrenheita,
- ustawić temperaturę przez podanie wartości w stopniach Fahrenheita.

Przy ustawianiu wartości należy odpowiednio przeliczyć ją i zapisać wewnętrznie w stopniach Celsjusza.

#### 5. Atrybut `kelvin`

Klasa ma udostępniać atrybut `kelvin`, który pozwala:

- odczytać temperaturę w kelwinach,
- ustawić temperaturę przez podanie wartości w kelwinach.

Przy ustawianiu wartości należy odpowiednio przeliczyć ją i zapisać wewnętrznie w stopniach Celsjusza.

#### 6. Walidacja danych

Należy zadbać o to, aby nie dało się ustawić temperatury w kelwinach mniejszej niż 0.

Jeżeli użytkownik spróbuje ustawić wartość fizycznie niemożliwą, program powinien ustawić temperaturę na 0 K.

Można przyjąć, że warunek ten powinien być pilnowany niezależnie od tego, czy użytkownik ustawia wartość przez `celsius`, `fahrenheit`, czy `kelvin`.

#### 7. Reprezentacja tekstowa obiektu

Klasa powinna posiadać czytelną reprezentację tekstową, np. przez implementację `__repr__` lub `__str__`.

Przykładowo, obiekt może być prezentowany w postaci:

```python
Temperature(25.0°C)
```

albo w innej sensownej, czytelnej formie.

### Przykładowe użycie

Program powinien poprawnie działać dla sytuacji podobnych do poniższych:

```python
t = Temperature(25)

print(t.celsius)      # 25
print(t.fahrenheit)   # 77.0
print(t.kelvin)       # 298.15

t.fahrenheit = 32
print(t.celsius)      # 0.0

t.kelvin = 300
print(t.celsius)      # 26.85

t.kelvin = -300      
print(t.kelvin)      # 0
```

### Wymagania dodatkowe

Do podstawowej wersji zadania należy dodać przynajmniej **dwa** z poniższych rozszerzeń.

#### Wariant A - właściwość tylko do odczytu

Dodaj atrybut, którego nie da się ustawiać, a jedynie odczytywać, np.:

- `is_freezing` - zwraca `True`, jeśli temperatura jest mniejsza lub równa 0°C,
- `is_boiling` - zwraca `True`, jeśli temperatura jest większa lub równa 100°C.

#### Wariant B - stan skupienia wody

Dodaj atrybut `state`, która zwraca napis określający stan skupienia wody przy normalnym ciśnieniu:

- `'solid'` dla temperatur poniżej 0°C,
- `'liquid'` dla temperatur od 0°C do poniżej 100°C,
- `'gas'` dla temperatur równych lub większych niż 100°C.

#### Wariant C - metoda klasowa lub statyczna

Dodaj metodę pomocniczą pozwalającą utworzyć obiekt na podstawie temperatury w innej skali, np.:

```python
t = Temperature.from_fahrenheit(68)
```

albo:

```python
t = Temperature.from_kelvin(273.15)
```

Nie mówiliśmy do tej pory o `@classmethod` i `@staticmethod`. Poczytajcie w dokumentacji o co chodzi.

#### Wariant D - działania na obiektach

Można dodać możliwość porównywania obiektów `Temperature` i
zaimplementować przeciążenie operatorów, np. dodawanie lub odejmowanie temperatury od temperatury.

---

## Zadanie 3 - generator liczb pseudolosowych

### Cel zadania

Celem zadania jest przećwiczenie tworzenia **generatorów** w Pythonie oraz zrozumienie, w jaki sposób funkcja wykorzystująca `yield` może zwracać kolejne wartości krok po kroku, bez tworzenia całej sekwencji od razu w pamięci.

W tym zadaniu należy zaimplementować własny generator liczb pseudolosowych oparty na prostym wzorze rekurencyjnym - implementujemy więc generator (w sensie Pythona) który jest jednocześniej generatorem (w sensie matematycznym) liczb pseudolosowych.

### Treść zadania

Należy napisać funkcję-generator, która generuje kolejne liczby pseudolosowe przy użyciu **liniowego generatora kongruencyjnego**.

Generator ma działać zgodnie ze wzorem:

$$
x_{n+1} = (a x_n + c) \bmod m
$$

gdzie:

- $x_n$ - bieżąca wartość ciągu,
- $x_{n+1}$ - kolejna wartość,
- $a$ - mnożnik,
- $c$ - przyrost,
- $m$ - moduł,
- `seed` - wartość początkowa, czyli $x_0$.

Funkcja ma być generatorem, a więc ma zwracać kolejne wartości przy użyciu `yield`.

### Wymagania podstawowe

#### 1. Implementacja generatora

Należy napisać funkcję, na przykład:

```python
def lcg(seed, a, c, m, N):
    ...
```

która po każdym kolejnym użyciu (w sensie generatora) zwraca następną wartość ciągu.

Generator ma działać aż do momentu, w którym użytkownik wygeneruje $N$ liczb.

#### 2. Demonstracja działania

W programie należy pokazać użycie generatora na co najmniej dwa sposoby:

- przez ręczne pobieranie kilku wartości funkcją `next()` (przeczytajcie w dokumentacji jak to działa),
- przez użycie pętli `for`.

### Wymagania dodatkowe

Przygotuj dodatkowy generator albo tryb działania, w którym zamiast liczb całkowitych z zakresu od `0` do `m - 1`, zwracane są liczby zmiennoprzecinkowe z przedziału:

$$
[0, 1)
$$

Można to uzyskać przez odpowiednie przeskalowanie wygenerowanej liczby.

### Przykład działania

Dla przykładowych parametrów:

- `seed = 1`
- `a = 5`
- `c = 3`
- `m = 16`

kolejne wartości są wyznaczane następująco:

$$
x_0 = 1
$$

$$
x_1 = (5 \cdot 1 + 3) \bmod 16 = 8
$$

$$
x_2 = (5 \cdot 8 + 3) \bmod 16 = 11
$$

$$
x_3 = (5 \cdot 11 + 3) \bmod 16 = 10
$$

i tak dalej.

Program powinien umożliwić wygenerowanie i wypisanie takich wartości.

### Wskazówki

- Kluczowym elementem zadania jest użycie `yield`, a nie zwykłego `return`.
- Nie korzystamy z modułu `random`. Chodzi o własną implementację prostego mechanizmu generowania liczb pseudolosowych.

### Dla chętnych

Osoby, które chcą zrobić coś więcej, mogą spróbować zrobić wykres kolejnych par wygenerowanych liczb przez taki generator - $(x_0, x_1), (x_1, x_2), (x_2, x_3), \ldots$. Pokazuje on dobitnie, dlaczego ten generator jest do bani.

---

## Zadanie 4 (dla hardkorów) - własna wersja `@property` z użyciem deskryptorów

Należy zaimplementować własny mechanizm działający podobnie do `@property`, oparty na **deskryptorach**.

Celem jest przygotowanie rozwiązania, które pozwala zdefiniować metody getter i setter, a następnie korzystać z nich składnią właściwą dla dostępu do zwykłego atrybutu o jakiejś nazwie (jak `@property`).

### Wymagania

Należy przygotować własną klasę realizującą odpowiedni deskryptor oraz pokazać jej użycie na przykładzie co najmniej jednej klasy użytkowej.

Rozwiązanie powinno umożliwiać zapis i odczyt w stylu 

```python
obj.value
obj.value = 10
```

przy jednoczesnym wykorzystaniu mechanizmu metod gettera i settera (jak `@property`).

### Oczekiwania

Rozwiązanie powinno zawierać:

1. implementację własnego odpowiednika `@property`,
2. sensowny przykład użycia.

### Uwagi

- Nie wolno używać w rozwiązaniu wbudowanego `@property`.
- Należy oprzeć rozwiązanie na mechanizmie deskryptorów.

