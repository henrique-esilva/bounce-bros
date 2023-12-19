import pygame
from pygame.locals import *
import graphics, math

class AnimationClass():

	def __init__(self):

		self.idle = Animation()
		self.walking = Animation()
		self.breaking = Animation()


class LiteAnimation():
	def __init__(self):
		self.sprite = None
		self.repeteco = False
		self.rodando = False
		self.index = 0

	def configura(self, inicioDoLoop):
		self.inicioDoLoop = inicioDoLoop


class Animation():

	def __init__(self):

		self.content = []
		self.repeteco = 0
		self.rodando = False
		self.index = 0


	def configura(self, inicioDoLoop):

		"""putting an integer will set an index sprite for second time play
		putting False will set the animation playing just once"""
		self.repeteco = inicioDoLoop

	def set(self, path, start = 0, end = 999 ):

		self.path = path
		self.content = graphics.import_animation( path, start, end )

	def turnOn(self):

		self.rodando = True
		self.index = 0

	def turnOff(self):

		self.rodando = False

	def configura_repeteco(self, arg): #remover funcao configura_repeteco()
		"""deprecated"""
		self.repetindo = arg

	def run(self, velocidade = 12):

		if velocidade == False:
			velocidade = 1
		else:
			a = math.copysign(velocidade, 1)
			velocidade = a/14

		if velocidade == 0: velocidade = 1

		if self.rodando:

			self.index += velocidade *0.5
			if math.floor( self.index ) >= len(self.content):
				if type(self.repeteco)==int:
					self.index = self.repeteco
				else:
					self.index=0
					self.turnOff()

	def goto( self, frame:int ):
		self.index = frame

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
			print( 'len(self.content) = ' + str(len(self.content)) + '\n' )
			sys.exit()
