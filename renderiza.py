import pygame, os
from pygame.locals import *

import screen_size
import color

pygame.init()





size = screen_size.size
pre_size = screen_size.pre_size

pre_tela = pygame.surface.Surface(pre_size)
pre_tela_rect = pre_tela.get_rect()

mini_tela = pygame.Surface( (pre_size[0]/2,pre_size[1]) )

os.environ["SDL_VIDEO_CENTERED"] = "1"

pygame.display.set_caption(" Jump Tales ")
os.environ["SDL_VIDEO_CENTERED"] = "1"

flags = pygame.SCALED
screen = pygame.display.set_mode(size)
#pygame.display.toggle_fullscreen()



def impressao_de_imagem( superficie, imagem, rect, rel_coord=(0,0) ):
    """carimba 'imagem' em 'superficie'.
    'rect' possui o tamanho da 'imagem' e coordenada.
    'rel_coord' e' a coordenada relativa da personagem referencia"""
    j=Rect(rect)
    j.move_ip(rel_coord)
    superficie.blit( imagem, j )


def renderiza_inversao_giro( a, superficie=pre_tela, rel_coord=(0, 0) ):
    imagem = pygame.transform.flip( a.current_animation.retorna_quadro(), a.left, 0 )
    imagem = pygame.transform.rotate( imagem, a.fisica.angulo_de_rotacao )
    rect = imagem.get_rect()
    rect.center = a.rect.center
    impressao_de_imagem( superficie, imagem , rect, rel_coord )


def renderiza_personagem( a, superficie=pre_tela, rel_coord=(0, 0) ):
    imagem = pygame.transform.flip( a.current_animation.retorna_quadro(), a.left, 0 )
    imagem = pygame.transform.rotate( imagem, a.fisica.angulo_de_rotacao )
    rect = imagem.get_rect()
    rect.center = a.rect.center
    impressao_de_imagem( superficie, imagem , rect, rel_coord )


def renderiza_particula( a, superficie=pre_tela, rel_coord=(0, 0) ):
    impressao_de_imagem( superficie, a.current_animation.retorna_quadro(), a.rect, rel_coord )


def renderiza_tiles( vetor, image, superficie=pre_tela, rel_coord=(0,0)):
    """Get a vetor of coordinates, and pygame.Surface image, a pygame.Surface
    screen and a relative coordinate rel_coord
    Make sure that all coordinates have bidimentional format (x, y)

    relative coordinate is used to move the image before rendering"""
    for i in vetor:
        j=Rect(i)
        j.move_ip(rel_coord)
        superficie.blit(image, j)


def renderiza_quadrados( vetor, tam, superficie=pre_tela, rel_coord=(0,0) ):
    for i in vetor:
        j=Rect(i[0]*tam[0], i[1]*tam[1], tam[0], tam[1])
        j.move_ip(rel_coord)
        pygame.draw.rect( superficie, color.colorDarkGrey, j, width = 0 )


def renderiza_tilesetpack(tilesetpack, superficie, rel_coord, tam):
    for i in tilesetpack[1]:
        superficie.blit(tilesetpack[0], (i[0]*tam[0]+rel_coord[0], i[1]*tam[1]+rel_coord[1]))


def renderiza_multitela():
    pre_tela.blit( mini_tela, (pre_size[0]/2, 0) )
    screen.blit( pygame.transform.scale(pre_tela, size), pygame.Rect(0, 0, 0, 0))
    pygame.display.flip()
    mini_tela.fill( (15, 15, 18) )
    pre_tela.fill(color.colorBlueyGrey)


def renderiza_tela():
    screen.blit( pygame.transform.scale(pre_tela, size), pygame.Rect(0, 0, 0, 0))
    pygame.display.flip()
    pre_tela.fill(color.colorGrey)
