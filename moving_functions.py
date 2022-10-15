import pygame
from pygame.locals import *

import screen_size
import renderiza

import objetos
import efeitos_visuais

import math

size = screen_size.size
pre_size = screen_size.pre_size


pygame.init()


def direction(arg): #verificar para onde está indo (direita esquerda)
    if arg.distiny[0] - arg.center[0] < 0:
        return 1
    else:
        return 0

def is_moving(arg):
    range_x = arg.distiny[0] - arg.center[0]
    range_y = arg.distiny[1] - arg.center[1]

    a = ((range_x ** 2) + (range_y ** 2)) ** 0.5

    if a == 0:
        a = 1
    elif a < 0:
        a = -a

    #sin = range_y / a
    #cos = range_x / a

    #speedx = arg.speed * cos
    #speedy = arg.speed * sin

    #arg.center[0] += speedx
    #arg.center[1] += speedy

    if a > arg.speed:
        return 1
    else:
        return 0

def move(arg):

    range_x = arg.distiny[0] - arg.center[0]
    range_y = arg.distiny[1] - arg.center[1]

    a = ((range_x ** 2) + (range_y ** 2)) ** 0.5

    if a == 0:
        a = 1
    elif a < 0:
        a = -a

    sin = range_y / a
    cos = range_x / a

    speedx = arg.speed * cos
    speedy = arg.speed * sin

    arg.center[0] += speedx
    arg.center[1] += speedy

    # E entao, arredondamos o resultado:

    if a > arg.speed:
        arg.rect.centerx =  int(arg.center[0])
        arg.rect.centery =  int(arg.center[1])



def mouse_control(arg):
    mouse = pygame.mouse.get_pressed()
    if mouse[0] or mouse[2]:
        pos = list(pygame.mouse.get_pos())

        pos[0] = pos[0]/screen_size.scale
        pos[1] = pos[1]/screen_size.scale

        arg.distiny = pos.copy()


def is_landed( coisa ):
    landed = False

    for plataforma in objetos.plataformas: # [ retangulo1 , retangulo2, retangulo3, ... ]
        if coisa.fisica.retangulo_do_corpo.colliderect( plataforma ):
            if coisa.rect.bottom - coisa.fisica.velocidade_de_queda <= plataforma.top +1 and coisa.fisica.velocidade_de_queda >= 0:
                landed = True

    if landed:
        return True
    elif coisa.rect.bottom < renderiza.pre_tela.get_rect().height:
        return False

    return True


def efeito_de_giro( kk ):
    if is_landed( kk ):
        kk.fisica.angulo_de_rotacao = 0
        kk.fisica.velocidade_de_rotacao = 0
    else:
        kk.fisica.velocidade_de_rotacao = -kk.fisica.velocidade_lateral
        kk.fisica.angulo_de_rotacao += kk.fisica.velocidade_de_rotacao


def controle_lateral_pula ( kk , key_set ):

    key_set = (
        (K_a, K_d, K_w),
        (K_LEFT, K_RIGHT, K_UP)
        )[key_set]

    limite_de_velocidade = 28

    tecla = pygame.key.get_pressed()

    if tecla[key_set[2]]:
        if is_landed( kk ):
            objetos.particulas.append( efeitos_visuais.ObjetoEfemero( [ kk.rect.centerx, kk.rect.bottom ] ) )
            kk.fisica.velocidade_de_queda = -18 -math.copysign( kk.fisica.velocidade_lateral, 1 )

    if tecla[key_set[0]]:
        kk.left = True
        kk.fisica.velocidade_lateral -= 2

    if tecla[key_set[1]]:
        kk.left = False
        kk.fisica.velocidade_lateral += 2

    # verificando se a velocidade estrapolou os limites...
    if kk.fisica.velocidade_lateral > limite_de_velocidade:
        kk.fisica.velocidade_lateral = limite_de_velocidade
    if kk.fisica.velocidade_lateral < -limite_de_velocidade:
        kk.fisica.velocidade_lateral = -limite_de_velocidade

    # verificando se nenhuma das teclas esta sendo pressionada...
    if not ( tecla[key_set[0]] or tecla[key_set[1]] ) and is_landed( kk ):

        #olhamos se a velocidade é para a direita ou esquerda...
        if kk.fisica.velocidade_lateral > 0:
            # então diminuimos...
            kk.fisica.velocidade_lateral -= 2
        if kk.fisica.velocidade_lateral < 0:
            # ...ou aumentamos     =^-^=
            kk.fisica.velocidade_lateral += 2
        if kk.fisica.velocidade_lateral == 1:
            kk.fisica.velocidade_lateral = 0

    # e por ultimo movemos
    kk.rect.centerx += kk.fisica.velocidade_lateral

    # aqui estou corrigindo
    # por ultimo, depois de mover o personagem, 
    # fazemos um reajuste de posição que impede
    # que alguém saia da tela

    kk.ajusta_retangulos()

    if kk.fisica.retangulo_do_corpo.right > renderiza.pre_tela_rect.width:
        kk.rect.centerx += renderiza.pre_tela_rect.width - kk.fisica.retangulo_do_corpo.right
        kk.fisica.velocidade_lateral = 0
    if kk.fisica.retangulo_do_corpo.left < 0:
        kk.rect.left -= kk.fisica.retangulo_do_corpo.left
        kk.fisica.velocidade_lateral = 0

    '''if kk.rect.left > renderiza.pre_tela_rect.width:
        kk.rect.right -= renderiza.pre_tela_rect.width + kk.rect.width
    if kk.rect.right < 0:
        kk.rect.left += renderiza.pre_tela_rect.width + kk.rect.width'''

    kk.ajusta_retangulos()


def colisao_com_plataformas( personagem, vetor_plataformas ):
    for plataforma in vetor_plataformas: # [ retangulo1 , retangulo2, retangulo3, ... ]

        personagem.ajusta_retangulos()

        if personagem.fisica.retangulo_do_corpo.colliderect( plataforma ):

            if personagem.rect.bottom - personagem.fisica.velocidade_de_queda <= plataforma.top +1 and personagem.fisica.velocidade_de_queda >= 0: #math.copysign( personagem.fisica.velocidade_lateral , 1 ):

                personagem.rect.bottom = plataforma.top +1
                personagem.fisica.velocidade_de_rotacao = 0
                personagem.fisica.angulo_de_rotacao     = 0
                personagem.fisica.velocidade_de_queda   = 0

            elif personagem.fisica.velocidade_de_queda < 0 and personagem.fisica.retangulo_do_corpo.top - personagem.fisica.velocidade_de_queda >= plataforma.bottom -1:

                personagem.rect.centery += plataforma.bottom -1 - personagem.fisica.retangulo_do_corpo.top
                personagem.fisica.velocidade_de_queda = 0

            else:

                # neste caso, a velocidade lateral de 'personagem' tem um módulo maior que a velocidade de queda.
                # Vamos mover o retangulo_de_colisao de 'personagem' na direção correspondente ao oposto indicado
                # pelo sinal de sua velocidade e no valor da diferença entre a lateral esquerda de seu
                # retângulo de colisão e a lateral direita da plataforma em questão.

                # se formos mover para a direita, neste caso a velocidade está negativa;
                # então o copysign ficará positivo.
                # usaremos a lateral direita da plataforma e a lateral esquerda do personagem.

                    # usar o sinal do copysign
                lateral_direita_da_plataforma = plataforma.centerx + plataforma.width /2

                    # usar o sinal inverso do copysign
                lateral_esquerda_da_personagem = personagem.rect.centerx - personagem.rect.width /2

                # se queremos mover a personagem para a direita, usaremos a subtração da lateral direita da
                # plataforma pela lateral esquerda da personagem.

                sinal = math.copysign( 1 , -personagem.fisica.velocidade_lateral )

                x = (plataforma.centerx + sinal * plataforma.width /2 ) - (personagem.fisica.retangulo_do_corpo.centerx - sinal * personagem.fisica.retangulo_do_corpo.width /2)

                personagem.rect.move_ip( x + sinal , 0 )

                personagem.fisica.velocidade_lateral = 0


def controla_setas(kk):
    tecla = pygame.key.get_pressed()

    if tecla[K_UP]:
        kk.rect.centery -= 1
    if tecla[K_LEFT]:
        kk.rect.centerx -= 4
    if tecla[K_DOWN]:
        kk.rect.centery += 1
    if tecla[K_RIGHT]:
        kk.rect.centerx += 4

def controla_wasd(kk):
    tecla = pygame.key.get_pressed()
    
    if tecla[K_w]:
        kk.rect.centery -= 1

    if tecla[K_s]:
        kk.rect.centery += 1

    if tecla[K_a]:
        kk.left = 1
        kk.rect.centerx -= 4

    if tecla[K_d]:
        kk.left = 0
        kk.rect.centerx += 4

def gravidade( coisa ):


    if not is_landed( coisa ):

        coisa.fisica.velocidade_de_queda += 3


    coisa.rect.bottom += coisa.fisica.velocidade_de_queda


    if coisa.rect.bottom > renderiza.pre_tela.get_rect().height:
        coisa.fisica.velocidade_de_queda = 0
        coisa.rect.bottom = renderiza.pre_tela.get_rect().height



def rebate( kk ):

    if kk.fisica.velocidade_de_queda > 0:
        for i in objetos.personagens:
            if i != kk:
                if kk.fisica.retangulo_dos_pes.colliderect( i.fisica.retangulo_da_cabeca ):
                    kk.rect.bottom = i.fisica.retangulo_da_cabeca.top

                    velocidade_do_kk = kk.fisica.velocidade_de_queda
                    kk.fisica.velocidade_de_queda = -20 + i.fisica.velocidade_de_queda - math.copysign( kk.fisica.velocidade_lateral, 1 )

                    #inverte a velocidade de queda para dar o efeito de impulso
                    i.fisica.velocidade_de_queda = -i.fisica.velocidade_de_queda + velocidade_do_kk
                    #i.vidas -= 1


def movimentacao_automatica_cossenoidal( coisa ):
    try:
        mov = coisa.movimentacao_cossenoidal
    except AttributeError:
        print( "ATENÇÃO: uma classe tentou usar a função de movimentação cossenoidal automática sem possuir a classe de atibutos \"Movimentacao_cossenoidal\"" )
        print( "O programa pode se desligar ou apresentar comportamento imprevisível por conta disso" )

    mov.espaco_angular += mov.velocidade_angular * 0.04
    mov.posicao_relativa = mov.amplitude_maxima * math.cos( mov.espaco_angular * math.pi)
    coisa.fisica.velocidade_lateral = mov.posicao_relativa

    coisa.left = math.sin( mov.espaco_angular * math.pi ) > 0

    coisa.rect.centerx = mov.posicao_relativa + mov.posicao_referencial