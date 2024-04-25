import pygame
from pygame.locals import *
import sys, math

db={}

def import_animation(arg, start = 0, end = 999):     # O "arg"(parametro) deve ser o nome do diretório + "\\" + nome da animação. E PRONTO. O subprograma faz o resto
	"""retorna um list de elementos pygame.Surface
	Forneça um 'arg' contendo o caminho da pasta de busca
	As imagens devem ter o nome no seguinte formato:
		frame + índice de 0000 até 9999 + .png
	Opcional fornecer start e end, indicando o inicio e fim da busca
	A busca será realizada ignorando falhas até encontrar uma imagem
	Após encontrar o primeiro elemento, qualquer tentativa falha
	encerra a função e retorna os quadros encontrados
	Retorna um list vazio após não encontrar nada
	"""
	a = []

	for i in range ( start , end ):
		try:
			patch = arg + ("\\frame%04d.png" % i)    # Aqui é criada uma string do caminho da imagem
			a.append(          pygame.image.load( patch )          )    # Aqui a imagem é importada
		except:
			if len(a) > 0: break

	if len(a) == 0:
		print('\nAVISO: \'import_animation()\' retornando vetor de comprimento nulo para:')
		print('\n\tcaminho de busca: \'' + arg + '\'\n\tindice: \''+str(start)+' '+str(end)+'\'')
		print('\n\tarquivos não encontrados')
	return a


class AnimationClass():

	def __init__(self):

		self.idle = Animation()
		self.walking = Animation()
		self.breaking = Animation()
		self.current = self.idle

		self.db = {
			'idle': self.idle,
			'walking': self.walking,
			'default': self.idle,
			'breaking': self.breaking
	    }

	def altera( self, arg ):
		if arg.lower() in self.db:
			self.db[arg.lower()].index = (self.db[arg.lower()].index,0)[int(self.current!=self.db[arg.lower()])]
			self.current = self.db[arg.lower()]


class Animation():

	def __init__(self):

		self.content = []
		self.repeteco = 0
		self.rodando = False
		self.index = 0

	def end_f(self):
		pass

	def configura(self, repeteco):
		self.repeteco = repeteco

	def set(self, path = None, start = 0, end=999):
		# a ideia aqui era a de atribuir um caminho (path) para cada animacao, o caminho seria salvo num banco de
		# imagens junto com o conteudo da animacao. Caso o path nao esteja no banco, a classe deve incluir no ban
		# co, o path como sendo uma chave, apontando para o conteudo da animacao, como sendo um valor. Caso o pat
		# h ja esteja no banco, a classe apenas aponta o seu content para o valor do path no banco.
		# Deste modo, todas as animacoes com o mesmo path terao o mesmo conteudo, sem repeticao na memoria

		self.path = path
		if path in db.keys():
			self.content = db[path]
		else:
			db[path] = import_animation( path , start, end )
			self.content = db[path]

	def turnOn(self):

		self.rodando = True
		self.index = 0

	def turnOff(self):

		self.rodando = False

	def configura_repeteco(self, arg):
		'''deprecated'''
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
