import pygame
from pygame.locals import *

tamanho_dos_tiles = ( 96, 96 )#(64, 64) #(96, 96)

tileset = [
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

for i in range(7, 20):
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
        tileset.remove(( x, y))

plataformas = [
]

for i in tileset:
    plataformas.append(
        pygame.Rect( tamanho_dos_tiles[0]*i[0], tamanho_dos_tiles[1]*i[1], tamanho_dos_tiles[0], tamanho_dos_tiles[1] )
    )