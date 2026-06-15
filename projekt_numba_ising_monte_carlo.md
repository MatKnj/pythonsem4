# Zadanie - Monte Carlo dla modelu Isinga z użyciem Numba

## Cel zadania

Celem zadania jest zaimplementowanie symulacji Monte Carlo dwuwymiarowego modelu Isinga na siatce $N \times N$ w dwóch wersjach:

1. bez użycia Numba,
2. z użyciem Numba.

Następnie należy porównać czasy wykonania obu wersji oraz sprawdzić, jaki zysk wydajności daje kompilacja JIT.

Symulacja ma być wykonana dla:

- periodycznych warunków brzegowych,
- oddziaływania z 8 sąsiadami,
- spinów $s_{i} \in \{-1, +1\}$.

Po wykonaniu symulacji należy dodatkowo:

- przygotować animację ewolucji układu,
- narysować wykres magnetyzacji w funkcji czasu.

## Opis modelu

Rozważamy siatkę spinów $s_{i}$, gdzie każdy spin przyjmuje wartość $+1$ albo $-1$.

Hamiltonian układu ma postać

$$
H = -J \sum_{\langle i,j \rangle} s_i s_j - B \sum_i s_i,
$$

gdzie:

- $J$ - stała oddziaływania,
- $B$ - zewnętrzne pole magnetyczne,
- pierwsza suma biegnie po parach sąsiadujących spinów,
- w tym zadaniu każdy spin ma **8 sąsiadów**:
  - 4 sąsiadów w pionie i poziomie,
  - 4 sąsiadów po przekątnych.

Uwaga: ponieważ korzystamy z periodycznych warunków brzegowych, siatka "zawija się" na krawędziach.

## Zmiana energii przy odwróceniu spinu

W algorytmie Monte Carlo nie trzeba za każdym razem liczyć całej energii układu. Wystarczy policzyć zmianę energii przy próbie odwrócenia pojedynczego spinu.

Jeżeli próbujemy zmienić spin $s_{i} \to -s_{i}$, to zmiana energii wynosi

$$
\Delta E = E_1 - E_0.
$$

Dla modelu z polem zewnętrznym i oddziaływaniem z sąsiadami można ją zapisać jako

$$
\Delta E = 2 s_{i} \left( J \sum_{j \in \text{nn}} s_{j} + B \right),
$$

gdzie suma biegnie po wszystkich 8 sąsiadach spinu $s_{i}$.

## Algorytm Monte Carlo

Należy zastosować algorytm Metropolisa.

Dla każdej próby zmiany spinu:

1. losujemy położenie (spin) $i$ na siatce,
2. obliczamy $\Delta E$ dla próby odwrócenia spinu $s_{i}$,
3. jeżeli $\Delta E < 0,$ to akceptujemy zmianę zawsze,
4. jeżeli $\Delta E > 0,$ to akceptujemy zmianę z prawdopodobieństwem
    $$
    p(\Delta E) = e^{-\beta \Delta E},
    $$
    gdzie
    $$
    \beta = \frac{1}{kT}.
    $$

    W tym zadaniu traktujemy $\beta$ jako parametr wejściowy.

## Makrokrok

W zadaniu przez **jeden krok symulacji** rozumiemy **makrokrok**, czyli wykonanie liczby prób zmiany spinu równej $N^2.$

Innymi słowy, jeden makrokrok odpowiada średnio jednej próbie aktualizacji na każdy spin w układzie.

Jeżeli liczba makrokroków wynosi $M$, to całkowita liczba elementarnych prób zmiany spinu jest równa $M=N^2.$

## Parametry symulacji

Program powinien umożliwiać ustawienie następujących parametrów:

- $N$ - rozmiar siatki, czyli układ $N \times N$,
- $J$ - stała oddziaływania,
- $\beta$ - parametr temperaturowy,
- $B$ - zewnętrzne pole magnetyczne,
- $M$ - liczba makrokroków.

## Wymagania implementacyjne

Należy przygotować:

### 1. Wersję bez Numba

Zwykła implementacja w Pythonie z użyciem NumPy tam, gdzie to wygodne, ale bez dekoratorów Numba.

### 2. Wersję z Numba

Przyspieszona wersja programu z użyciem Numba, na przykład z dekoratorem `@njit`.

Warto zadbać o to, aby obie wersje realizowały dokładnie ten sam algorytm i różniły się jedynie sposobem wykonania.

## Co należy zapisać w czasie symulacji

W trakcie działania programu należy rejestrować przynajmniej:

- stan siatki w kolejnych makrokrokach lub wybrane zapisane klatki,
- magnetyzację całkowitą układu,
- energię całkowitą układu.

Magnetyzację można zdefiniować jako

$$
m(t) = \frac{1}{N^2} \sum_{i} s_{i}.
$$

Dzięki temu otrzymujemy wielkość z przedziału od $-1$ do $1$.

## Wizualizacja wyników

Po wykonaniu symulacji należy przygotować:

### 1. Animację

Animację ewolucji konfiguracji spinów w czasie, na przykład z użyciem `matplotlib.animation.FuncAnimation`.


### 2. Wykres magnetyzacji

Wykres magnetyzacji $m(t)$ w funkcji numeru makrokroku.

Na wykresie oś pozioma powinna odpowiadać numerowi makrokroku, a oś pionowa magnetyzacji.

### 4. Wykres energii

Wykres energii całkowitej układu $H(t)$ w funkcji numeru makrokroku.

Na wykresie oś pozioma powinna odpowiadać numerowi makrokroku, a oś pionowa energii.


## Porównanie wydajności

Należy zmierzyć czas wykonania obu wersji programu:

- wersji bez Numba,
- wersji z Numba.

Porównanie należy przeprowadzić dla tych samych parametrów wejściowych.

Uwaga: przy pomiarze czasu dla wersji z Numba należy pamiętać, że **pierwsze wywołanie funkcji kompilowanej JIT zawiera koszt kompilacji**, więc warto ten fakt uwzględnić w interpretacji wyników.

## Sugestie techniczne

- Siatkę spinów można przechowywać jako dwuwymiarową tablicę wartości $-1$ i $+1$.
- Stan początkowy można przygotować losowo.
- Periodyczne warunki brzegowe można zaimplementować przez odpowiednie zawijanie indeksów.
- Warto wydzielić osobne funkcje do:
  - inicjalizacji siatki,
  - obliczania $\Delta E$,
  - wykonania jednego makrokroku,
  - uruchomienia całej symulacji,
  - obliczania magnetyzacji,
  - tworzenia animacji.

## Dodatkowe uwagi

Nie trzeba liczyć całkowitej energii układu po każdej elementarnej zmianie spinu, jeżeli poprawnie obliczana jest wartość $\Delta E$.
