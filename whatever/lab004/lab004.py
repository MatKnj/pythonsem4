import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

import ising_numba as ising
import argparse
import sys


parser = argparse.ArgumentParser(description='lab004 nie wiem co tu wpisać')

parser.add_argument('--N', type=int, help='Rozmiar N siatki NxN', default=100)
parser.add_argument('--M', type=int, help='Liczba makrokroków M', default=500)
parser.add_argument('--beta', type=float, help='Wartość parametru beta', default=0.4)
parser.add_argument('--B', type=float, help='Wartość pola B', default=0.0)
parser.add_argument('--J', type=float, help='Wartość parametru J', default=1.0)
parser.add_argument('--magnetization-file', type=str, 
                    help='Nazwa pliku, do którego zostanie zapisana magnetyzacja, w razie braku tego argumentu nie będzie ona nigdzie zapisana.'
                    )

parser.add_argument('--show-animation', action='store_true',
                    help='Flaga decydujaca o tym, czy wyświetlić animację symulacji.'
                    )
parser.add_argument('--animation-file', type=str, 
                    help='Nazwa pliku, do którego zostanie zapisana animacja, w razie braku tego argumentu nie będzie ona nigdzie zapisana.'
                    )


args = parser.parse_args()
zapis_magnetyzacji = False
zapis_animacji = False

try: 
    if args.N < 1:
        raise ValueError('Parametr N musi być większy od 0')
    if args.M < 1:
        raise ValueError('Parametr M musi być większy od 0')
    if args.beta <= 0:
        raise ValueError('Parametr beta musi być większy od 0')
    if args.magnetization_file is not None:
        if not args.magnetization_file.endswith('.txt'):
            raise ValueError('Plik musi mieć rozszerzenie .txt')
    if args.animation_file is not None:
        if not args.animation_file.endswith('.gif'):
            raise ValueError('Plik animacji musi mieć rozszerzenie .gif')
    
except ValueError as e:
    print('Wystąpił błąd: ', e)
    sys.exit(1)



print(args)

print('Parametry symulacji:')
print(f'N = {args.N}')
print(f'M = {args.M}')
print(f'beta = {args.beta}')
print(f'B = {args.B}')
print(f'J = {args.J}')


if args.magnetization_file is not None:
    print(f'Nazwa pliku docelowego (magnetyzacja): {args.magnetization_file}')
    zapis_magnetyzacji = True

if args.animation_file is not None:
    print(f'Nazwa pliku docelowego (animacja): {args.animation_file}')
    zapis_animacji = True
##################################################################

N = args.N
M = args.M
beta = args.beta
B = args.B
J = args.J
nazwa_pliku_magnetyzacji = args.magnetization_file
show_animation = args.show_animation
nazwa_pliku_animacji = args.animation_file


stany, energie, magnetyzacja = ising.symulacja(M, N, J, B, beta)

##################################################################

if zapis_magnetyzacji:

    t = []
    for i in range(len(magnetyzacja)):
        t.append(i)

    with open(nazwa_pliku_magnetyzacji, 'w') as plik:
        for krok, magn in zip(t, magnetyzacja):
            plik.write(f'{krok} {magn}\n')


##################################################################

if show_animation or zapis_animacji:
    fig = plt.figure(figsize=(4, 4))
    fig.subplots_adjust(left=0, right=1, bottom=0, top=1)
    plt.axis('off')

    img = plt.imshow(stany[0])

    def update(i):
        img.set_data(stany[i])
        return (img,)

    ani = FuncAnimation(
        fig,
        update,
        frames=len(stany),
        interval=50,
        blit=True
    )


    if zapis_animacji:
        ani.save(nazwa_pliku_animacji, writer='pillow', fps=20)

    if show_animation:
        plt.show()