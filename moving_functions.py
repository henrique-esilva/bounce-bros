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



def direction( arg ):
    #verifica para onde está indo (1=direita 0=esquerda)
    if arg.distiny[0] - arg.center[0] < 0:
        return 1
    else:
        return 0


def is_moving( arg ):
    range_x = arg.distiny[0] - arg.center[0]
    range_y = arg.distiny[1] - arg.center[1]

    a = ((range_x ** 2) + (range_y ** 2)) ** 0.5

    if a == 0:
        a = 1
    elif a < 0:
        a = -a

    if a > arg.speed:
        return 1
    else:
        return 0


def move( arg ):

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


def gravidade( coisa ):

    if coisa.fisica.afetado_por_gravidade:
        if not is_landed( coisa ):
            coisa.fisica.velocidade_de_queda += 3


    coisa.rect.bottom += coisa.fisica.velocidade_de_queda




def colisao_com_plataformas( personagem, vetor_plataformas = objetos.plataformas ):
    for plataforma in vetor_plataformas:

        personagem.ajusta_retangulos()

        intercessao = (
            plataforma.left+1 < personagem.fisica.retangulo_do_corpo.left -personagem.fisica.velocidade_lateral < plataforma.right-1 or
            plataforma.left+1 < personagem.fisica.retangulo_do_corpo.right -personagem.fisica.velocidade_lateral < plataforma.right-1
        )

        dist_relat = (
            + math.copysign( 1, personagem.fisica.velocidade_lateral )
            * ( personagem.fisica.retangulo_do_corpo.centerx
            + math.copysign( personagem.fisica.retangulo_do_corpo.width/2, personagem.fisica.velocidade_lateral )
            - personagem.fisica.velocidade_lateral )
            - math.copysign( 1, personagem.fisica.velocidade_lateral )
            * ( plataforma.centerx - math.copysign( plataforma.width /2, personagem.fisica.velocidade_lateral ) )
            )

        if personagem.fisica.retangulo_do_corpo.colliderect( plataforma ):

            if (
                personagem.rect.bottom > plataforma.top and personagem.rect.bottom - personagem.fisica.velocidade_de_queda <= plataforma.top +1 and
                personagem.fisica.velocidade_de_queda >= 0 and ( intercessao )
            ):

                personagem.rect.bottom = plataforma.top + 1
                personagem.fisica.velocidade_de_rotacao = 0
                personagem.fisica.angulo_de_rotacao     = 0
                personagem.fisica.velocidade_de_queda   = 0

            elif ( personagem.fisica.velocidade_de_queda < 0 and 
                personagem.fisica.retangulo_do_corpo.top - personagem.fisica.velocidade_de_queda
                >= plataforma.bottom -1 and intercessao ):

                personagem.rect.centery += plataforma.bottom - personagem.fisica.retangulo_do_corpo.top
                personagem.fisica.velocidade_de_queda = 0

            elif personagem.rect.bottom > plataforma.top + 1 and personagem.fisica.velocidade_lateral != 0 and (
                + math.copysign( 1, personagem.fisica.velocidade_lateral )
                * ( personagem.fisica.retangulo_do_corpo.centerx
                + math.copysign( personagem.fisica.retangulo_do_corpo.width /2, personagem.fisica.velocidade_lateral )
                - personagem.fisica.velocidade_lateral )
                - math.copysign( 1, personagem.fisica.velocidade_lateral )
                * ( plataforma.centerx - math.copysign( plataforma.width /2, personagem.fisica.velocidade_lateral ) )
                ) > 0:

                # neste caso, a velocidade lateral de 'personagem' tem um módulo maior que a velocidade de queda.
                # Vamos mover o retangulo_de_colisao de 'personagem' na direção correspondente ao oposto indicado
                # pelo sinal de sua velocidade e no valor da diferença entre a lateral esquerda de seu
                # retângulo de colisão e a lateral direita da plataforma em questão.

                # se formos mover para a direita, neste caso a velocidade está negativa;
                # então o copysign ficará positivo.
                # usaremos a lateral direita da plataforma e a lateral esquerda do personagem.

                    # usar o sinal do copysign
                #lateral_direita_da_plataforma = plataforma.centerx + plataforma.width /2

                    # usar o sinal inverso do copysign
                #lateral_esquerda_da_personagem = personagem.rect.centerx - personagem.rect.width /2

                # se queremos mover a personagem para a direita, usaremos a subtração da lateral direita da
                # plataforma pela lateral esquerda da personagem.

                sinal = math.copysign( 1 , personagem.fisica.velocidade_lateral )

                personagem.rect.centerx = sinal + ( plataforma.centerx - sinal * plataforma.width/2 ) - ( 
                    sinal * personagem.fisica.retangulo_do_corpo.width/2 )

                personagem.fisica.velocidade_lateral = 0

                personagem.ajusta_retangulos()
            
        personagem.ajusta_retangulos()


def rebate( kk:__build_class__ ):

    if kk.fisica.velocidade_de_queda > 0:
        for i in objetos.personagens + objetos.fantasminhas:
            if i != kk:
                if kk.fisica.retangulo_dos_pes.colliderect( i.fisica.retangulo_da_cabeca ) and kk.fisica.retangulo_dos_pes.bottom - kk.fisica.velocidade_de_queda < i.fisica.retangulo_da_cabeca.top:

                    kk.rect.bottom = i.fisica.retangulo_da_cabeca.top
                    kk.ajusta_retangulos()
                    velocidade_do_kk = kk.fisica.velocidade_de_queda

                    #if is_landed(i):
                    #    kk.fisica.velocidade_de_queda = -velocidade_do_kk

                    #else:
                        #media = int((velocidade_do_kk - i.fisica.velocidade_de_queda)/2)
                        #kk.fisica.velocidade_de_queda = -media-12
                        #i.fisica.velocidade_de_queda = media+12
                    kk.fisica.velocidade_de_queda = -25 + i.fisica.velocidade_de_queda - math.copysign( kk.fisica.velocidade_lateral, 1 ) * 1.5

                        #inverte a velocidade de queda para dar o efeito de impulso
                    i.fisica.velocidade_de_queda = -i.fisica.velocidade_de_queda + velocidade_do_kk
                    i.vidas -= 1
                    break

def is_landed( coisa ):
    landed = False

    for plataforma in objetos.plataformas: # [ retangulo1 , retangulo2, retangulo3, ... ]
        if coisa.fisica.retangulo_do_corpo.colliderect( plataforma ):

            intercessao = (
                plataforma.left+1 < coisa.fisica.retangulo_do_corpo.left -coisa.fisica.velocidade_lateral < plataforma.right-1 or
                plataforma.left+1 < coisa.fisica.retangulo_do_corpo.right -coisa.fisica.velocidade_lateral < plataforma.right-1
            )

            if ( coisa.rect.bottom - coisa.fisica.velocidade_de_queda <= plataforma.top +1 and 
                coisa.fisica.velocidade_de_queda >= 0 and intercessao ):
                landed = True
                break

    if landed:
        return True

    return False


def efeito_de_giro( kk ):
    if is_landed( kk ):
        kk.fisica.angulo_de_rotacao = 0
        kk.fisica.velocidade_de_rotacao = -kk.fisica.velocidade_lateral
    else:
        kk.fisica.velocidade_de_rotacao = -kk.fisica.velocidade_lateral
        kk.fisica.angulo_de_rotacao += kk.fisica.velocidade_de_rotacao


def desacelera_move_lateral_ajusta(kk):
    if is_landed( kk ) and kk.fisica.velocidade_lateral != 0:

        if math.copysign(kk.fisica.velocidade_lateral, 1) <= 1:
            kk.fisica.velocidade_lateral -= math.copysign( 1, kk.fisica.velocidade_lateral )

        elif math.copysign(kk.fisica.velocidade_lateral, 1) > 1:
            kk.fisica.velocidade_lateral -= math.copysign( 2, kk.fisica.velocidade_lateral )


    kk.rect.centerx += kk.fisica.velocidade_lateral
    kk.ajusta_retangulos()


def desaceleracao_aerea(kk):

    if kk.fisica.velocidade_lateral != 0:
        if math.copysign(kk.fisica.velocidade_lateral, 1) <= 1:
            kk.fisica.velocidade_lateral -= math.copysign( 1, kk.fisica.velocidade_lateral )

        elif math.copysign(kk.fisica.velocidade_lateral, 1) > 1:
            kk.fisica.velocidade_lateral -= math.copysign( 2, kk.fisica.velocidade_lateral )

    if kk.fisica.velocidade_de_queda != 0:
        if math.copysign(kk.fisica.velocidade_de_queda, 1) <= 1:
            kk.fisica.velocidade_de_queda = 0
            #= math.copysign( 1, kk.fisica.velocidade_de_queda )

        elif math.copysign(kk.fisica.velocidade_de_queda, 1) > 1:
            kk.fisica.velocidade_de_queda -= math.copysign( 2, kk.fisica.velocidade_de_queda )

    kk.rect.centerx += kk.fisica.velocidade_lateral
    kk.ajusta_retangulos()


def movimento_aereo_passivo(kk):
    kk.rect.centerx += kk.fisica.velocidade_lateral
    kk.ajusta_retangulos()


def move_lateral_ajusta(kk):
    kk.rect.centerx += kk.fisica.velocidade_lateral
    kk.ajusta_retangulos()


def controle_lateral_pula ( kk , key_set, limite = 30 ):

    key_set = (
        (K_a, K_d, K_w),
        (K_LEFT, K_RIGHT, K_UP)
        )[key_set]

    limite_de_velocidade = limite

    tecla = pygame.key.get_pressed()

    if tecla[key_set[2]]:
        if is_landed( kk ):
            objetos.particulas.append( efeitos_visuais.ObjetoEfemero( [ kk.rect.centerx, kk.rect.bottom ] ) )
                # 30 is needed to jump a plataform
            kk.fisica.velocidade_de_queda = kk.multiplicadores_de_salto[0] - math.copysign( kk.fisica.velocidade_lateral, 1 ) * kk.multiplicadores_de_salto[1]
            #if kk.fisica.velocidade_lateral >= kk.multiplicadores_de_velocidade[0]:
            kk.fisica.velocidade_lateral = kk.fisica.velocidade_lateral * kk.multiplicadores_de_velocidade[1][math.copysign(kk.fisica.velocidade_lateral,1) == kk.multiplicadores_de_velocidade[0]]

    if tecla[key_set[0]]:
        if kk.fisica.velocidade_lateral > -limite_de_velocidade:
            kk.fisica.velocidade_lateral -= 1

    if tecla[key_set[1]]:
        if kk.fisica.velocidade_lateral < limite_de_velocidade:
            kk.fisica.velocidade_lateral += 1

    # verificando se a velocidade estrapolou os limites...
    if is_landed(kk):
        if kk.fisica.velocidade_lateral > limite_de_velocidade:
            kk.fisica.velocidade_lateral = limite_de_velocidade
        if kk.fisica.velocidade_lateral < -limite_de_velocidade:
            kk.fisica.velocidade_lateral = -limite_de_velocidade

    # verificando se nenhuma das teclas esta sendo pressionada...
    if is_landed( kk ) and ( ( tecla[key_set[0]] and tecla[key_set[1]] ) or (not ( tecla[key_set[0]] or tecla[key_set[1]] )) or ( not tecla[key_set[0]] and kk.fisica.velocidade_lateral < 0) or ( not tecla[key_set[1]] and kk.fisica.velocidade_lateral > 0)):

        # olhamos se a velocidade é para a direita ou esquerda...

        #abs=math.copysign(kk.fisica.velocidade_lateral, 1)
        kk.fisica.velocidade_lateral -= math.copysign(int(kk.fisica.velocidade_lateral!=0), kk.fisica.velocidade_lateral)
        kk.fisica.velocidade_lateral -= math.copysign(int(kk.fisica.velocidade_lateral!=0), kk.fisica.velocidade_lateral)

        #if kk.fisica.velocidade_lateral > 0:
        #    # então diminuimos...
        #    kk.fisica.velocidade_lateral -= 2
        #if kk.fisica.velocidade_lateral < 0:
        #    # ...ou aumentamos     =^-^=
        #    kk.fisica.velocidade_lateral += 2
        #if kk.fisica.velocidade_lateral == 1:
        #    kk.fisica.velocidade_lateral = 0


    kk.left = ( 
        kk.fisica.velocidade_lateral < 0 
        ) or kk.left * (
        kk.fisica.velocidade_lateral == 0 )
    #if kk.fisica.velocidade_lateral > 0: kk.left = False
    #elif kk.fisica.velocidade_lateral < 0: kk.left = True

    # e movemos
    kk.rect.centerx += kk.fisica.velocidade_lateral

    kk.ajusta_retangulos()



def controle_voo( personagem, key_set, limite = 30 ):
    key_set = (
        (K_a, K_d, K_w, K_s),
        (K_LEFT, K_RIGHT, K_UP, K_DOWN)
        )[key_set]
    
    limite_de_velocidade = limite
    tecla = pygame.key.get_pressed()

    if tecla[key_set[0]]:
        personagem.fisica.velocidade_lateral -= 1

    if tecla[key_set[1]]:
        personagem.fisica.velocidade_lateral += 1

    if not (tecla[key_set[0]] or tecla[key_set[1]]) and personagem.fisica.velocidade_lateral != 0:
        personagem.fisica.velocidade_lateral -= math.copysign( 1, personagem.fisica.velocidade_lateral )

    if tecla[key_set[2]]:
        personagem.fisica.velocidade_de_queda -= 1

    if tecla[key_set[3]]:
        personagem.fisica.velocidade_de_queda += 1

    if not (tecla[key_set[2]] or tecla[key_set[3]]) and personagem.fisica.velocidade_de_queda != 0:
        personagem.fisica.velocidade_de_queda -= math.copysign( 1, personagem.fisica.velocidade_de_queda )


    # verificando se a velocidade estrapolou os limites...
    #personagem.fisica.velocidade_lateral = ( personagem.fisica.velocidade_lateral * (personagem.fisica.velocidade_lateral in range(-limite_de_velocidade, limite_de_velocidade))) + (math.copysign(limite_de_velocidade, personagem.fisica.velocidade_lateral) * (not personagem.fisica.velocidade_lateral in range(-limite_de_velocidade, limite_de_velocidade))) # is this better?

    if personagem.fisica.velocidade_lateral > limite_de_velocidade:
        personagem.fisica.velocidade_lateral = limite_de_velocidade
    if personagem.fisica.velocidade_lateral < -limite_de_velocidade:
        personagem.fisica.velocidade_lateral = -limite_de_velocidade

    if personagem.fisica.velocidade_de_queda > limite_de_velocidade:
        personagem.fisica.velocidade_de_queda = limite_de_velocidade
    if personagem.fisica.velocidade_de_queda < -limite_de_velocidade:
        personagem.fisica.velocidade_de_queda = -limite_de_velocidade

    personagem.left = ( 
        personagem.fisica.velocidade_lateral < 0 
        ) or personagem.left * (
        personagem.fisica.velocidade_lateral == 0 )
    personagem.rect.centerx += personagem.fisica.velocidade_lateral

    personagem.ajusta_retangulos()


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


def loop_dentro_da_tela( kk ):
    if kk.rect.left > renderiza.pre_tela_rect.width:
        kk.rect.right -= renderiza.pre_tela_rect.width + kk.rect.width
    if kk.rect.right < 0:
        kk.rect.left += renderiza.pre_tela_rect.width + kk.rect.width


def movimentacao_automatica_cossenoidal( coisa ):
    try:
        mov = coisa.movimentacao_cossenoidal
    except AttributeError:
        print( "ATENÇÃO: uma classe tentou usar a função de movimentação cossenoidal automática sem possuir a classe de atibutos \"Movimentacao_cossenoidal\"" )
        print( "O programa pode se desligar ou apresentar comportamento imprevisível por conta disso\n" )

    posicao_relativa_anterior = int(mov.amplitude_maxima * math.cos( mov.espaco_angular * math.pi))
    mov.espaco_angular += mov.velocidade_angular * 0.04
    mov.posicao_relativa = int(mov.amplitude_maxima * math.cos( mov.espaco_angular * math.pi))
    coisa.fisica.velocidade_lateral = mov.posicao_relativa - posicao_relativa_anterior

    coisa.left = math.sin( mov.espaco_angular * math.pi ) > 0

    coisa.rect.centerx += coisa.fisica.velocidade_lateral
    coisa.ajusta_retangulos()

    #coisa.rect.centerx = mov.posicao_relativa + mov.posicao_referencial


def movimentacao_automatica_senoidal( coisa ):
    try:
        mov = coisa.movimentacao_senoidal
    except AttributeError:
        print( "ATENÇÃO: uma classe tentou usar a função de movimentação cossenoidal automática sem possuir a classe de atibutos \"Movimentacao_senoidal\"" )
        print( "O programa pode se desligar ou apresentar comportamento imprevisível por conta disso\n" )

    posicao_relativa_anterior = int(mov.amplitude_maxima * math.cos( mov.espaco_angular * math.pi))
    mov.espaco_angular += mov.velocidade_angular * 0.04
    mov.posicao_relativa = int(mov.amplitude_maxima * math.cos( mov.espaco_angular * math.pi))
    coisa.fisica.velocidade_de_queda = mov.posicao_relativa - posicao_relativa_anterior

    coisa.rect.centery += coisa.fisica.velocidade_de_queda
    coisa.ajusta_retangulos()