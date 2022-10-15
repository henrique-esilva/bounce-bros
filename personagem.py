import pygame, sys
from pygame.locals import *

import graphics, math




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
		self.current_animation = None


		self.center = [0, 0]
		self.rect = pygame.Rect( 0, 0, 50, 50 )


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


	def run(self):

		if self.fisica.velocidade_lateral == 0:
			self.current_animation = self.animations.idle
		else:
			if self.current_animation == self.animations.idle:
				self.animations.walking.turnOn()
			self.current_animation = self.animations.walking

		# ajustando o retângulo de colisão global
		self.fisica.retangulo_do_corpo.bottom = self.rect.bottom
		self.fisica.retangulo_do_corpo.centerx = self.rect.centerx

		# ajustando o retangulo de colisão da cabeça da personagem
		self.fisica.retangulo_da_cabeca.bottom = self.rect.bottom - 57
		self.fisica.retangulo_da_cabeca.centerx = self.rect.centerx

		# ajustando o retangulo de colisão dos pés da personagem
		self.fisica.retangulo_dos_pes.bottom = self.rect.bottom
		self.fisica.retangulo_dos_pes.centerx = self.rect.centerx




class Fisica():
	def __init__(self):
		self.velocidade_lateral = 0
		self.velocidade_de_queda = 0

		self.velocidade_de_rotacao = 0
		self.angulo_de_rotacao = 0

		self.retangulo_do_corpo = pygame.Rect( 0, 0, 35, 72 )

		# O retangulo da cabeça deve ficar 57px acima da borda inferior do retangulo principal
		self.retangulo_da_cabeca = pygame.Rect( 0, 0, 35, 17 )

		self.retangulo_dos_pes = pygame.Rect( 0, 0, 35, 30 )



class AnimationClass():

	def __init__(self):

		self.idle = Animation()
		self.walking = Animation()



class Animation():

	def __init__(self):

		self.content = []
		self.inicioDoLoop = 0
		self.repetindo = True
		self.rodando = False
		self.index = 0

	def configura(self, inicioDoLoop):
		self.inicioDoLoop = inicioDoLoop

	def set(self, path = None):

		if path:

			self.path = path
			self.content = graphics.import_animation( path )
		else:

			try:

				self.content = graphics.import_animation( self.path )
			except AttributeError:
				print('\nWARNING: Animation() class in Animation.set() function')
				print('    recebendo valor nulo para o caminho de diretório!')
				print('    resulta em tentativa falha de auto-incrementação\n')
				print('    erro iminente!\n')

	def turnOn(self):

		self.rodando = True
		self.index = 0

	def turnOff(self):

		self.rodando = False

	def configura_repeteco(self, arg):
		
		self.repetindo = arg

	def run(self):

		if self.rodando:

			self.index += 0.5
			if math.floor( self.index ) >= len(self.content):
				try:
					if self.repetindo:
						self.index = self.inicioDoLoop
					else:
						self.turnOff()
						self.index = 0

				except AttributeError:
					print('WARNING: erro de atribuição de instância em \'Animation.run()\'')
					print('    configure a classe de animação!')
					sys.exit()

	def retorna_quadro(self):

		try:
			if self.rodando:
				return self.content[math.floor( self.index )]
			else:
				return pygame.surface.Surface( (0, 0) )

		except IndexError:
			print( '\nWARNING: \'index\' invalido para -> \'Animation\' em \'retorna_valor()\'' )
			print( 'index =', self.index )
			print( 'efetivo =', math.floor( self.index ) )
			print( 'len(self.content) = ' + str(len(self.content)) + '\n')
			sys.exit()


murasaki = Personagem()

murasaki.animations.idle.set( 'characters//murasaki//idle' )
murasaki.animations.idle.configura(0)
murasaki.animations.idle.turnOn()

murasaki.animations.walking = Animation()
murasaki.current_animation = murasaki.animations.walking
murasaki.current_animation.set( 'characters//murasaki//andando' )
murasaki.current_animation.configura(6)
murasaki.current_animation.turnOn()

murasaki.rect = murasaki.animations.walking.content[0].get_rect()
murasaki.rect.left = 0


drexa = Personagem()

drexa.current_animation = drexa.animations.idle
drexa.current_animation.set( 'characters//drexa//ataque' )
drexa.current_animation.configura(0)
drexa.current_animation.turnOn()


drexa.current_animation = drexa.animations.walking
drexa.current_animation.set( 'characters//drexa//walking' )
drexa.current_animation.configura(0)
drexa.current_animation.turnOn()

drexa.rect = drexa.current_animation.content[0].get_rect()
drexa.rect.right = 800


'''slime = Personagem()

slime.current_animation = slime.animations.idle
slime.current_animation.set( '../../Pietro/slime' )
slime.current_animation.configura(0)
slime.current_animation.turnOn()

slime.animations.walking = slime.animations.idle'''


monstrinho = Personagem()
monstrinho.movimentacao_cossenoidal = Movimentacao_cossenoidal(500)
monstrinho.movimentacao_cossenoidal.set_frequencia( 0.3 )
monstrinho.movimentacao_cossenoidal.set_amplitude( 100 )

monstrinho.current_animation = monstrinho.animations.idle
monstrinho.current_animation.set( 'characters\pequeno mago\idle' )
monstrinho.current_animation.configura(0)
monstrinho.current_animation.turnOn()

monstrinho.animations.walking.set( 'characters\pequeno mago\idle' )
monstrinho.animations.walking.configura(0)
monstrinho.animations.walking.turnOn()

monstrinho.rect = monstrinho.animations.idle.content[0].get_rect()
monstrinho.rect.left = 500
monstrinho.rect.bottom = 100


personagens = [ murasaki, drexa ]
