import pygame
from pygame.locals import *

tamanho_dos_tiles = ( 96, 96 ) #(64, 64) #(96, 96)

tileset = [
    # colunas
    (-2, 5),
    (-2, 4),
    (-2, 3),
    (-2, 2),
    (-1, 2),
    ( 0, 2),
    ( 1, 5),
    (-2, 6),
    (-1, 6),
    ( 0, 6),
    ( 1, 6),
    ( 2, 6),
    ( 3, 6),
    ( 4, 6),

    ( 5, 3),
    ( 6, 3),
    ( 7, 3),

    ( 6, 4),
    ( 7, 4),
    ( 7, 5),
]
tileset.extend([
    # chão comprido
    (7, 6), (8, 6), (9, 6), (10, 6), (11, 6), (12, 6), (13, 6), (14, 6), (15, 6), (16, 6), (17, 6), (18, 6), (19, 6)
])
tileset.extend([
    # sala com escada
    (-2, 7), (-2, 8), (-2, 9), (-2, 10), (-2, 11), (-1, 7), (-1, 11), (0, 7), (0, 11), (1, 7), (1, 11), (2, 7), (2, 11), (3, 7), (3, 10), (3, 11), (4, 9), (4, 10), (4, 11), (5, 8), (5, 9), (5, 10), (5, 11), (6, 7), (6, 8), (6, 9), (6, 10), (6, 11)
])

'''for i in range(7, 20):
    tileset.append((i, 6))

for x in range(-2, 7):
    for y in range(7, 12):
        tileset.append((x, y))

tileset.remove(( 5, 7))
tileset.remove(( 4, 7))
for x in range(4):
    for y in range(3-x):
        tileset.remove((2+x, 8+y))
for x in range(-1, 2):
    for y in range( 8,11):
        tileset.remove(( x, y))'''

tileset.sort()
tileset.reverse()

plataformas = [
]

for i in tileset:
    plataformas.append(
        pygame.Rect( tamanho_dos_tiles[0]*i[0], tamanho_dos_tiles[1]*i[1], tamanho_dos_tiles[0], tamanho_dos_tiles[1] )
    )