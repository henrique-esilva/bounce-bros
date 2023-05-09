import pygame, os
from pygame.locals import *

import screen_size
import color

pygame.init()





size = screen_size.size
pre_size = screen_size.pre_size

pre_tela = pygame.surface.Surface(pre_size)
pre_tela_rect = pre_tela.get_rect()

mini_tela = pygame.Surface((pre_size[0]/2,pre_size[1]))

os.environ["SDL_VIDEO_CENTERED"] = "1"

pygame.display.set_caption(" Jump Tales =^-^= ")
os.environ["SDL_VIDEO_CENTERED"] = "1"

flags = pygame.SCALED
screen = pygame.display.set_mode(size, flags)
#pygame.display.toggle_fullscreen()



def impressao_de_imagem( superficie, imagem, rect, rel_coord=(0,0) ):
    j=Rect(rect)
    j.move_ip(rel_coord)
    superficie.blit( imagem, j )


def renderiza_personagem( a, superficie=pre_tela, rel_coord=(0, 0) ):
    #retangulo_de_posicao = a.rect
    imagem = pygame.transform.flip( a.current_animation.retorna_quadro(), a.left, 0 )
    imagem = pygame.transform.rotate( imagem, a.fisica.angulo_de_rotacao )
    rect = imagem.get_rect()
    rect.center = a.rect.center
    impressao_de_imagem( superficie, imagem , rect, rel_coord )


def renderiza_particula( a, superficie=pre_tela, rel_coord=(0, 0) ):
    impressao_de_imagem( superficie, a.current_animation.retorna_quadro(), a.rect, rel_coord )


def renderiza_tiles( vetor, superficie=pre_tela, rel_coord=(0,0) ):
    for i in vetor:
        j=Rect(i)
        j.move_ip(rel_coord)
        pygame.draw.rect( superficie, color.colorDarkGrey, j, width = 0 )

def renderiza_tela():
    pre_tela.blit( mini_tela, (size[0]/2, 0) )
    screen.blit( pygame.transform.scale(pre_tela, size), pygame.Rect(0, 0, 0, 0))
    pygame.display.flip()
    mini_tela.fill(color.colorOrange)
    pre_tela.fill((0, 255, 0))
