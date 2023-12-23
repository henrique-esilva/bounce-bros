import pygame
from functools import partial
from animation import *
from fisica import Fisica

class Elemento():
	animations = AnimationClass()
	def __init__(self):
		self.comportamento=[]
		self.fisica = Fisica()
	def run(self):
		for i in range(len(self.comportamento)):
			self.comportamento[i](self)
	def ajusta_retangulos( self ):

		# ajustando o retângulo de colisão global
		self.fisica.retangulo_do_corpo.bottom = self.rect.bottom
		self.fisica.retangulo_do_corpo.centerx = self.rect.centerx

		# ajustando o retangulo de colisão da cabeça da personagem
		self.fisica.retangulo_da_cabeca.bottom = self.rect.bottom - 57
		self.fisica.retangulo_da_cabeca.centerx = self.rect.centerx

		# ajustando o retangulo de colisão dos pés da personagem
		self.fisica.retangulo_dos_pes.bottom = self.rect.bottom
		self.fisica.retangulo_dos_pes.centerx = self.rect.centerx

	def default_animation_adjust(self):
		if self.fisica.velocidade_lateral == 0:
			if self.current_animation != self.animations.idle:
				self.animations.idle.turnOn()
			self.current_animation = self.animations.idle
		else:
			if len( self.animations.breaking.content ) and ( self.fisica.velocidade_lateral > 0 ) == self.left:
				self.current_animation = self.animations.breaking
			elif len(self.animations.walking.content) > 0:
				if self.current_animation != self.animations.walking:
					self.animations.walking.turnOn()
				self.current_animation = self.animations.walking

# espada arremessada é o objeto que será swmmonado quando Murasaki arremesar sua lâmina
# ela rodopia no ar
# ao colidir com uma parede, sua velocidade se inverte
# ao colidir com o chão ela muda de comportamento

class EspadaVoadora(Elemento):

	def __init__(self, left=0):
		super().__init__()
		self.animations.idle.set('efeitos//espada//girando')
		self.animations.idle.configura(0)
		self.animations.idle.turnOn()

		self.animations.fly = Animation()
		self.animations.fly.set('efeitos//espada//girando')
		self.animations.fly.configura(0)
		self.animations.fly.turnOn()

		self.current_animation = self.animations.fly
		self.on_stop = self.delme

		self.graus = 0
		self.pos = (0, 0)
		self.left = left

		self.rect = pygame.Rect(0, 0, 64, 64)

	def delme(self):
		self.ref.remove(self)


def giraespada(espada):
	espada.image = pygame.transform.rotate(espada.originalimage, espada.graus)
