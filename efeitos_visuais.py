import pygame
from pygame.locals import *

from personagem import Animation




animacoes = {
    'fumaca': '../efects/fumaca/padrao/'
}


class ObjetoEfemero ():

    def __init__(self, posicao, path = '../efects/fumaca/padrao/' ):
        self.current_animation = Animation()

        self.current_animation.set( path )
        self.current_animation.configura(0)
        self.current_animation.turnOn()
        self.current_animation.configura_repeteco( False )



        self.rect = self.current_animation.content[0].get_rect()
        self.rect.centerx = posicao[0]
        self.rect.bottom  = posicao[1]
