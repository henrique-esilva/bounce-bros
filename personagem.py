import pygame, sys
from pygame.locals import *

from animation import *
from fisica import Fisica

pygame.mixer.init()


class Movimentacao_cossenoidal():
	def __init__( self , posicao_referencial ):
		# unidade de medida de espaço angular = pi * radianos
		# frequencia deve ser em hertz
		self.amplitude_maxima = 100
		self.frequencia = 1
		self.espaco_angular = 0 # vai de 0 (ZERO) até 2 (em pi radianos)
		self.velocidade_angular = 2 * self.frequencia

			# não deve ser alterada
		self.posicao_referencial = posicao_referencial

			# deve ser alterada a cada frame
		self.posicao_relativa = 0

	def set_frequencia( self , frequencia ):
		self.frequencia = frequencia
		self.velocidade_angular = 2 * self.frequencia

	
	def set_amplitude( self, amplitude ):
		self.amplitude_maxima = amplitude




class Personagem():

	def __init__(self):

		self.vidas = 5
		self.fisica = Fisica()
		self.left = False


		self.animations = AnimationClass()
		self.current_animation = self.animations.idle


		self.center = [0, 0]
		self.rect = pygame.Rect( 0, 0, 50, 50 )
		self.funcoes = []

		self.modo_de_controle = ( None, None )

		# temporario
		#self.running_sound = pygame.mixer.Sound(file='sound\effects\walky/ocarina.wav')
		#self.running_sound.set_volume(0.1)


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

	def running_sound_play(self, *args):
		if self.fisica.velocidade_lateral != 0 and self.fisica.velocidade_de_queda==0:
			if self.running_sound.get_num_channels()==0:
				self.running_sound.play(-1, maxtime=1200)
		else:
			self.running_sound.stop()

	def run(self):

		#if self.fisica.velocidade_lateral == 0:
		#	if self.current_animation != self.animations.idle:
		#		self.animations.idle.turnOn()
		#	self.current_animation = self.animations.idle
		#else:
		#	if len( self.animations.breaking.content ) and ( self.fisica.velocidade_lateral > 0 ) == self.left:
		#		self.current_animation = self.animations.breaking
		#	elif len(self.animations.walking.content) > 0:
		#		if self.current_animation != self.animations.walking:
		#			self.animations.walking.turnOn()
		#		self.current_animation = self.animations.walking

		self.default_animation_adjust()

		# ajustando o retângulo de colisão global
		self.fisica.retangulo_do_corpo.bottom = self.rect.bottom
		self.fisica.retangulo_do_corpo.centerx = self.rect.centerx

		# ajustando o retangulo de colisão da cabeça da personagem
		self.fisica.retangulo_da_cabeca.bottom = self.rect.bottom - 57
		self.fisica.retangulo_da_cabeca.centerx = self.rect.centerx

		# ajustando o retangulo de colisão dos pés da personagem
		self.fisica.retangulo_dos_pes.bottom = self.rect.bottom
		self.fisica.retangulo_dos_pes.centerx = self.rect.centerx

		for i in self.funcoes:
			i( self )



'''
class Fisica():
	def __init__(self):
		self.velocidade_lateral = 0
		self.velocidade_de_queda = 0
		self.afetado_por_gravidade = True

		self.velocidade_de_rotacao = 0
		self.angulo_de_rotacao = 0

		self.retangulo_do_corpo = pygame.Rect( 0, 0, 36, 77 )

		# O retangulo da cabeça deve ficar 57px acima da borda inferior do retangulo principal
		self.retangulo_da_cabeca = pygame.Rect( 0, 0, 36, 17 )

		self.retangulo_dos_pes = pygame.Rect( 0, 0, 36, 30 )
'''




murasaki = Personagem()

murasaki.animations.idle.set( 'characters//murasaki//idle', 26)
murasaki.animations.idle.configura(0)
murasaki.animations.idle.turnOn()

murasaki.current_animation = murasaki.animations.idle

murasaki.animations.walking.set( 'characters//murasaki//andando-lento', 9 )
murasaki.animations.walking.configura(0)
murasaki.animations.walking.turnOn()

murasaki.animations.fast_walking = Animation()
murasaki.animations.fast_walking.set( 'characters//murasaki//andando', 23 )
murasaki.animations.fast_walking.configura(0)
murasaki.animations.fast_walking.turnOn()

murasaki.animations.breaking.set( 'characters//murasaki//andando', 59 )
murasaki.animations.breaking.configura(0)
murasaki.animations.breaking.turnOn()

# I will make a `slash` animation for murasaki. Will have also a function to attack, that switches
# the current animation for `slash` and places a object in scene that deals damage to enemies.

murasaki.rect = murasaki.animations.walking.content[0].get_rect()
murasaki.rect.left = 0

def murasaki_animation_extra_adjust( blabla:any ):
	if math.copysign( murasaki.fisica.velocidade_lateral, 1 ) >= 10:
		murasaki.current_animation = murasaki.animations.fast_walking
#murasaki.funcoes.insert( 1, murasaki_animation_extra_adjust )

drexa = Personagem()

drexa.current_animation = drexa.animations.idle
drexa.current_animation.set( 'characters//drexa//new//idle', 32, 63 )
drexa.current_animation.configura(0)
drexa.current_animation.turnOn()


drexa.current_animation = drexa.animations.walking
drexa.current_animation.set( 'characters//drexa//new//walk', 24 )
drexa.current_animation.configura(0)
drexa.current_animation.turnOn()

drexa.rect = drexa.current_animation.content[0].get_rect()
drexa.rect.left = 300


logan = Personagem()

logan.animations.idle.set( 'characters//drexa//logan//idle' )
logan.animations.idle.configura(0)
logan.animations.idle.turnOn()
logan.animations.walking.set( 'characters//drexa//logan//walk' )
logan.animations.walking.configura(0)
logan.animations.walking.turnOn()

logan.rect=logan.current_animation.content[0].get_rect()
logan.rect.left=180


arquimago = Personagem()
arquimago.current_animation = arquimago.animations.idle
arquimago.current_animation.set( 'characters\\arquimago\idle' )
arquimago.current_animation.configura(0)
arquimago.current_animation.turnOn()

arquimago.rect = arquimago.current_animation.content[0].get_rect()
arquimago.rect.left = 300
arquimago.fisica.afetado_por_gravidade = False


monstrinho = Personagem()
monstrinho.movimentacao_cossenoidal = Movimentacao_cossenoidal(600)
monstrinho.movimentacao_cossenoidal.set_frequencia( 0.2 )
monstrinho.movimentacao_cossenoidal.set_amplitude( 100 )

monstrinho.movimentacao_senoidal = Movimentacao_cossenoidal(600)
monstrinho.movimentacao_senoidal.set_frequencia( 0.4 )
monstrinho.movimentacao_senoidal.set_amplitude( 96 )
monstrinho.movimentacao_senoidal.espaco_angular = 0

monstrinho.current_animation = monstrinho.animations.idle
monstrinho.current_animation.set( 'characters//boca//flutuando', 76 ) # 'characters\\boca\idle-fly' ) #pequeno mago\idle' )
monstrinho.current_animation.configura(0)
monstrinho.current_animation.turnOn()

#monstrinho.animations.walking.set( 'characters\\boca\\flutuando', 76 ) #pequeno mago\idle' )
#monstrinho.animations.walking.configura(0)
#monstrinho.animations.walking.turnOn()

#monstrinho.rect = monstrinho.animations.idle.content[0].get_rect()
monstrinho.rect.top = 96+28
monstrinho.rect.left = 1000
monstrinho.fisica.retangulo_do_corpo.width = 30


boca=Personagem()
boca.animations.idle.set( 'characters\\boca\\flutuando', 76 )
boca.animations.idle.configura(0)
boca.animations.idle.turnOn()

boca.rect.centerx= -96*3.5
boca.rect.top= 96+28

boca.movimentacao_senoidal = Movimentacao_cossenoidal(600)
boca.movimentacao_senoidal.set_frequencia( 0.4 )
boca.movimentacao_senoidal.set_amplitude( 96 )
boca.movimentacao_senoidal.espaco_angular = 0


maguinho = Personagem()

maguinho.current_animation = maguinho.animations.idle
maguinho.current_animation.set( 'characters\\boca\\flutuando', 76 ) #( 'characters\\boca\\flutuando' ) #pequeno mago\idle' )
maguinho.current_animation.configura(0)
maguinho.current_animation.turnOn()

#maguinho.animations.walking.set( 'characters\\boca\\walk-fly' )
#maguinho.animations.walking.configura(0)
#maguinho.animations.walking.turnOn()


maguinho.fisica.afetado_por_gravidade = False
maguinho.rect = maguinho.animations.idle.content[0].get_rect()
maguinho.rect.left = 400
maguinho.rect.bottom = 100

cyber = Personagem()
cyber.current_animation = cyber.animations.idle
cyber.current_animation.set( 'characters\\cyber\\walking' )
cyber.current_animation.content = cyber.animations.idle.content[:1]
cyber.current_animation.configura(0)
cyber.current_animation.turnOn()
cyber.current_animation = cyber.animations.walking
cyber.current_animation.set( 'characters\\cyber\\walking', 1 )
cyber.current_animation.configura(1)
cyber.rect = cyber.animations.idle.content[0].get_rect()
cyber.current_animation.turnOn()
cyber.rect.left = 250

personagens = [ murasaki, drexa, logan, cyber, arquimago, maguinho ]