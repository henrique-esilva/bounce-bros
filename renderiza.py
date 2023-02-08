import pygame, os
from pygame.locals import *

import screen_size
import color

import moving_functions

pygame.init()





size = screen_size.size
pre_size = screen_size.pre_size

pre_tela = pygame.surface.Surface(pre_size)
pre_tela_rect = pre_tela.get_rect()

os.environ["SDL_VIDEO_CENTERED"] = "1"

pygame.display.set_caption(" Jump Tales =^-^= ")
os.environ["SDL_VIDEO_CENTERED"] = "1"

flags = pygame.SCALED
screen = pygame.display.set_mode(size, flags)
#pygame.display.toggle_fullscreen()





def renderiza_personagem( a ):
    retangulo_de_posicao = a.rect
    imagem = pygame.transform.flip( a.current_animation.retorna_quadro(), a.left, 0 )
    imagem = pygame.transform.rotate( imagem, a.fisica.angulo_de_rotacao )
    rect = imagem.get_rect()
    rect.center = retangulo_de_posicao.center
    pre_tela.blit( imagem , rect )


def renderiza_particula( a ):
    retangulo_de_posicao = a.rect
    pre_tela.blit( a.current_animation.retorna_quadro() , retangulo_de_posicao )


def renderiza_tiles( vetor ):
    for i in vetor:
        pygame.draw.rect( pre_tela, color.colorDarkGrey, i, width = 0 )


def renderiza_tela():
    screen.blit( pygame.transform.scale(pre_tela, size), pygame.Rect(0, 0, 0, 0))
    pygame.display.flip()
    pre_tela.fill(color.colorGrey)
