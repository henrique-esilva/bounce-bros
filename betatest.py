#from personagem import murasaki, drexa, arquimago, cyber, maguinho, logan, mandy
from renderiza import *
from moving_functions import *
#from functools import partial
#from math import copysign as cs
from random import randint
import objetos
from tileset import array as tileset_array, tamanho_dos_tiles

murasaki, drexa, arquimago, cyber, maguinho, logan, mandy = objetos.murasaki, objetos.drexa, objetos.arquimago, objetos.cyber, objetos.maguinho, objetos.logan, objetos.mandy

def config_fantasmas():
	objetos.monstrinho.funcoes.append( movimentacao_automatica_senoidal )
	objetos.monstrinho2.funcoes.append( perseguir_localmente )
	#objetos.monstrinho2.funcoes.append( colisao_com_plataformas )
	objetos.boca.funcoes.append( movimentacao_automatica_senoidal )
	objetos.monstrinho2.perseguicao_local.alvos = objetos.personagens

imagem_coracao = pygame.image.load( "efeitos\\coracao.png" )


def controle_adequado_efetivo1( character ):
    """controlar com awd"""
    character.modo_de_controle[0]( character, 0, character.modo_de_controle[1] )
def controle_adequado_efetivo2( character ):
    """controlar com <^>"""
    character.modo_de_controle[0]( character, 1, character.modo_de_controle[1] )
def controle_adequado_passivo( character ):
    """controle passivo automatico"""
    character.modo_de_controle[2]( character )
controle_adequado_efetivo = controle_adequado_efetivo1
def movimentacao_padrao( character, atividade:int ):
    """atividade 0 -> nao controla\n
    atividade 1 -> controle com awd\n
    atividade 2 -> controle com <^> (setas)"""
    (controle_adequado_passivo, controle_adequado_efetivo)[atividade](character)
    #(controle_adequado_passivo, controle_adequado_efetivo1, controle_adequado_efetivo2)[atividade](character)


def config_personagens():
	    # define conjunto de configuracao de controle ativo e passivo dos personagens
	    # assim: modo_de_controle = (funcao_de_controle_ativo, velocidade, funcao_de_controle_passivo)
	objetos.murasaki.modo_de_controle = ( controle_lateral_pula, 7, desacelera_move_lateral_ajusta )
	objetos.drexa.modo_de_controle = ( controle_lateral_pula, 6, desacelera_move_lateral_ajusta)
	objetos.cyber.modo_de_controle = ( controle_lateral_pula, 7, desacelera_move_lateral_ajusta )
	objetos.logan.modo_de_controle = ( controle_lateral_pula, 7, desacelera_move_lateral_ajusta )
	objetos.mandy.modo_de_controle = ( controle_lateral_pula, 13, desacelera_move_lateral_ajusta )
	objetos.arquimago.modo_de_controle = ( controle_voo, 8, desaceleracao_aerea )
	objetos.maguinho.modo_de_controle = ( controle_voo, 8, desaceleracao_aerea )

	    # salto base
	    # mulplicador de velocidade
	objetos.murasaki.multiplicadores_de_salto = (-29, 1  )
	objetos.drexa.   multiplicadores_de_salto = (-29, 1.5)
	objetos.cyber.   multiplicadores_de_salto = (-29, 0  )
	objetos.logan.   multiplicadores_de_salto = (-29, 1  )
	objetos.mandy.   multiplicadores_de_salto = (-30, 0.5)

	    # velocidade minima de ativacao
	    # multiplicador de velocidade adicional
	objetos.murasaki.multiplicadores_de_velocidade = (12, {False: 1, True:1  })
	objetos.drexa.   multiplicadores_de_velocidade = (12, {False: 1, True:1  })
	objetos.cyber.   multiplicadores_de_velocidade = ( 4, {False: 1, True:1  })
	objetos.logan.   multiplicadores_de_velocidade = ( 8, {False: 1, True:2  })
	objetos.mandy.   multiplicadores_de_velocidade = ( 5, {False: 1, True:1  })

	root_funcoes =       [gravidade, rebate, colisao_com_plataformas, efeito_de_giro]
	objetos.murasaki.funcoes +=  root_funcoes
	objetos.drexa.funcoes +=     root_funcoes
	objetos.arquimago.funcoes += [gravidade, colisao_com_plataformas]
	objetos.cyber.funcoes +=     root_funcoes
	objetos.maguinho.funcoes +=  [gravidade, colisao_com_plataformas]
	objetos.logan.funcoes +=     root_funcoes
	objetos.mandy.funcoes +=     root_funcoes


#objetos.monstrinho.funcoes.append( movimentacao_automatica_senoidal )
#objetos.monstrinho2.funcoes.append( perseguir_localmente )
##objetos.monstrinho2.funcoes.append( colisao_com_plataformas )
#objetos.boca.funcoes.append( movimentacao_automatica_senoidal )
config_fantasmas()


config_personagens()
#root_funcoes =       [gravidade, rebate, colisao_com_plataformas, efeito_de_giro]
#murasaki.funcoes +=  root_funcoes
#drexa.funcoes +=     root_funcoes
#arquimago.funcoes += [gravidade, colisao_com_plataformas]
#cyber.funcoes +=     root_funcoes
#maguinho.funcoes +=  [gravidade, colisao_com_plataformas]
#logan.funcoes +=     root_funcoes
#mandy.funcoes +=     root_funcoes


indice_player = 0
tempo_de_atraso_para_alternancia = 200
temporizador_de_atraso_de_alternancia = pygame.time.Clock()

def alternancia_personagem(arg):
    global indice_player
    global tempo_de_atraso_para_alternancia

    temporizador_de_atraso_de_alternancia.tick()
    if tempo_de_atraso_para_alternancia > 0:
        tempo_de_atraso_para_alternancia -= temporizador_de_atraso_de_alternancia.get_time()
    else:    
        if arg[pygame.K_RETURN]:
            indice_player += 1
            if indice_player >= len(objetos.personagens):
                indice_player = 0
            tempo_de_atraso_para_alternancia = 200
    if indice_player >= len(objetos.personagens):
        indice_player = len(objetos.personagens)-1

def gambiarra_espada(arg):
    if arg[K_SPACE]:
        objetos.swmmon_espada_voadora(
            player.rect.center,
            (
                {1: -10, 0:10}[player.left]+player.fisica.velocidade_lateral,
                -randint(10,18) +player.fisica.velocidade_de_queda
            ),
            [gravidade, colisao_com_plataformas, desacelera_move_lateral_ajusta, gatilho_islanded_delme, efeito_de_giro],
            player.left
        )


def move_todos_pela_tela():
    distancia_a_mover = pre_tela_rect.centerx - player.rect.centerx
    distancia_a_movery = pre_tela_rect.centery - player.rect.centery
    for i in objetos.personagens:
        i.rect.move_ip( distancia_a_mover, distancia_a_movery )
        i.ajusta_retangulos()
    for i in objetos.fantasminhas:
        i.rect.move_ip( distancia_a_mover, distancia_a_movery )
        i.ajusta_retangulos()
    for i in objetos.plataformas:
        i.move_ip( distancia_a_mover, distancia_a_movery )
    for i in objetos.particulas:
        i.rect.move_ip( distancia_a_mover, distancia_a_movery )


def desenha_coracoes():
    y = 0
    for i in objetos.personagens:
        x = 0
        for vida in range(i.vidas):
            #desenhar a imagem de coração
            pre_tela.blit( imagem_coracao, pygame.Rect( 5 + x * 16, 5 + y * 24, 0, 0 ) )
            x += 1
        y += 1

def remove_personagem( indice_player ):
    y = 0
    for i in objetos.personagens:
        for inimigo in objetos.fantasminhas:
            if i.fisica.retangulo_do_corpo.colliderect( inimigo.fisica.retangulo_do_corpo ):
                i.vidas = 0
        if i.vidas <= 0:
            i.vidas = 0
            if indice_player > y:
                indice_player -= 1
            objetos.adiciona_bandeira( (objetos.personagens[y].rect.centerx, objetos.personagens[y].rect.bottom) )
            objetos.personagens.pop( y )
        y += 1
    if not len(objetos.personagens): return True
    return False

def get_rel_char(char):
    return (pre_tela_rect.centerx - char.rect.centerx, pre_tela_rect.centery - char.rect.centery)

def main():

    global indice_player
    global player

    pressed_keys = pygame.key.get_pressed()

    alternancia_personagem(pressed_keys)
    #gambiarra_espada(pressed_keys)

    player = objetos.personagens[ indice_player ]
    #player2 = objetos.personagens[ indice_player-1 ]

    for character in objetos.personagens:
        movimentacao_padrao(character, int(character==player)) #+2*int(character==player2))

    rel_p1 = (get_rel_char(player ))

    for i in objetos.fantasminhas + objetos.personagens:
        i.current_animation.run()#i.fisica.velocidade_lateral )
        i.run()
        renderiza_personagem( i, pre_tela, rel_p1 )

    #rel_p1 = (get_rel_char(player ))#[0]-pre_size[0]/4, get_rel_char(player )[1])
    #rel_p2 = (get_rel_char(player2)[0]-pre_size[0]/4, get_rel_char(player2)[1])

    #for i in objetos.fantasminhas + objetos.personagens:
    #    renderiza_personagem( i, pre_tela, rel_p1 )
        #renderiza_personagem( i, mini_tela, rel_p2 )

    for i in objetos.obj_moveis:
        i.run()
        i.current_animation.run()
        renderiza_inversao_giro( i, pre_tela, rel_p1 )


    for i in objetos.particulas:

        if not i.current_animation.rodando:
            objetos.particulas.remove(i)

        i.current_animation.run()
        renderiza_particula( i, pre_tela, rel_p1 )
        #renderiza_particula( i, mini_tela, rel_p2 )

    void = remove_personagem(indice_player)

    for i in range(len(tileset_array)):
        renderiza_quadrados( tileset_array[i][1], tamanho_dos_tiles, pre_tela, rel_p1 )
    #    renderiza_tilesetpack( tileset_array[i], pre_tela, rel_p1, tamanho_dos_tiles )

    desenha_coracoes()

    if pressed_keys[K_LSHIFT]:
        renderiza.zoom_grad, zoom_shift = controle_zoom_shift(renderiza.zoom_grad, pressed_keys)
        pre_tela.blit( pygame.transform.scale( pre_tela.subsurface(renderiza.get_half_rect(zoom_shift)), pre_size ), (0, 0) )

    renderiza_tela()

    return void

