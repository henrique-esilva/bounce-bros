import pygame

class Fisica():
	def __init__(self):
		self.velocidade_lateral = 0
		self.velocidade_de_queda = 0
		self.afetado_por_gravidade = True

		self.coeficiente_de_rotacao = 1
		self.velocidade_de_rotacao = 0
		self.angulo_de_rotacao = 0

		self.retangulo_do_corpo = pygame.Rect( 0, 0, 25, 77 ) # width 36

		# O retangulo da cabeça deve ficar 57px acima da borda inferior do retangulo principal
		self.retangulo_da_cabeca = pygame.Rect( 0, 0, 25, 17 )

		self.retangulo_dos_pes = pygame.Rect( 0, 0, 25, 30 )
