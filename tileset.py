import pygame
from pygame.locals import *

tamanho_dos_tiles = ( 96, 96 ) #(64, 64) #(96, 96)

#isso vai para renderiza.py
__tilemappacks = []
#isso vai para objetos
plataformas = []

# crie uma array
# preencha esta array com pacotes de tilemap
# cada pacote terá uma imagem e várias coordenadas
# a imagem deverá ser exibida em cada coordenada do vetor durante o jogo
# as coordenadas deverão ser reposicionadas de acordo com a coordenada relativa da personagem

# monte um sistema de empacotamento de tilemap's
# desenvolva uma função que exiba a imagem em todas as coordenadas do tilemappack
# armazene os tilemappacks de maneira compacta

array = []

def settmpck(img_path, tileset:list):
	return ( pygame.image.load(img_path), tileset )

tilemappack_ground = []#(x, y) for x in range(-20, 20) for y in range(2, 4)]
#tilemappack_ground.extend([(-3, 1), (-5, 1)])

tilemappack_ground.extend([
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
    #( 4, 6),

    #( 5, 4),
    #( 6, 3),
    #( 7, 3),

    #( 6, 4),
    #( 7, 4),
    #( 7, 5),
])
tilemappack_ground.extend([
    # chão comprido
    #(7, 6), (8, 6), (9, 6), (10, 6), (11, 6), (12, 6), (13, 6), (14, 6), (15, 6), (16, 6), (17, 6), (18, 6), (19, 6)
    (x, 6) for x in range(7, 20)
])
tilemappack_ground.extend([
    # chão comprido inferior
    #(7, 6), (8, 6), (9, 6), (10, 6), (11, 6), (12, 6), (13, 6), (14, 6), (15, 6), (16, 6), (17, 6), (18, 6), (19, 6)
    (x, 7) for x in range(7, 20)
])
tilemappack_ground.extend([
    # sala com escada
    (-2, 7), (-2, 8), (-2, 9), (-2, 10), (-2, 11), (-1, 7), (-1, 11), (0, 7), (0, 11), (1, 7), (1, 11), (2, 7), (2, 11), (3, 10), (3, 11), (4, 9), (4, 10), (4, 11), (5, 8), (5, 9), (5, 10), (5, 11), (6, 7), (6, 8), (6, 9), (6, 10), (6, 11)
])



tilemappack_ground.sort()
tilemappack_ground.reverse()

for i in tilemappack_ground:
    plataformas.append(
        pygame.Rect( tamanho_dos_tiles[0]*i[0], tamanho_dos_tiles[1]*i[1], tamanho_dos_tiles[0], tamanho_dos_tiles[1] )
    )


tilemappack_ground = (pygame.image.load( "./tiles/terra-pedra_estendido.png" ), tilemappack_ground)

array.append(tilemappack_ground)
