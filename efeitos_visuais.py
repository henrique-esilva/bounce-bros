import pygame
from pygame.locals import *

from personagem import Animation
from graphics import import_animation


animacoes = {
    'efeitos/fumaca/': import_animation( 'efeitos/fumaca/' ),
    'efeitos/bandeira': import_animation( 'efeitos/bandeira/' )
}


class ObjetoEfemero ():

    def __init__(self, posicao, path = 'efeitos/fumaca/' ):

        self.current_animation = Animation()
        self.current_animation.content = animacoes[path]
        self.current_animation.configura( False )
        self.current_animation.turnOn()


        self.rect = self.current_animation.content[0].get_rect()
        self.rect.centerx = posicao[0]
        self.rect.bottom  = posicao[1]

class BandeiraDerrota ():

    def __init__( self, posicao ):
        self.current_animation = Animation()
        self.current_animation.content = animacoes['efeitos/bandeira']
        self.current_animation.configura( 8 )
        self.current_animation.turnOn()


        self.rect = self.current_animation.content[0].get_rect()
        self.rect.centerx = posicao[0]
        self.rect.bottom  = posicao[1]