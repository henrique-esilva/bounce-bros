from personagem import murasaki, drexa, arquimago, cyber, maguinho, logan
from renderiza import *
from moving_functions import *
from functools import partial
from math import copysign as cs
from random import randint
import objetos
from tileset import array as tileset_array, tamanho_dos_tiles

objetos.monstrinho.funcoes.append( movimentacao_automatica_senoidal )
#objetos.monstrinho.funcoes.append( movimentacao_automatica_cossenoidal )
objetos.boca.funcoes.append( movimentacao_automatica_senoidal )

imagem_coracao = pygame.image.load( "efeitos\\coracao.png" )

murasaki.modo_de_controle = ( controle_lateral_pula, 7, desacelera_move_lateral_ajusta )
drexa.modo_de_controle = ( controle_lateral_pula, 7, desacelera_move_lateral_ajusta)
cyber.modo_de_controle = ( controle_lateral_pula, 7, desacelera_move_lateral_ajusta )
logan.modo_de_controle = ( controle_lateral_pula, 7, desacelera_move_lateral_ajusta )
arquimago.modo_de_controle = ( controle_voo, 8, desaceleracao_aerea )
maguinho.modo_de_controle = ( controle_voo, 8, desaceleracao_aerea )

    # salto base
    # mulplicador de velocidade
murasaki.multiplicadores_de_salto = (-28, 1  )
drexa.   multiplicadores_de_salto = (-30, 1.5)
cyber.   multiplicadores_de_salto = (-30, 0  )
logan.   multiplicadores_de_salto = (-28, 1  )

    # velocidade minima de ativação
    # multiplicador de velocidade adicional
murasaki.multiplicadores_de_velocidade = (12, {False: 1, True:1  })
drexa.   multiplicadores_de_velocidade = (12, {False: 1, True:1  })
cyber.   multiplicadores_de_velocidade = ( 4, {False: 1, True:-2 })
logan.   multiplicadores_de_velocidade = ( 8, {False: 1, True:2  })

def controle_adequado_efetivo1( character ):
    character.modo_de_controle[0]( character, 0, character.modo_de_controle[1] )
def controle_adequado_efetivo2( character ):
    character.modo_de_controle[0]( character, 1, character.modo_de_controle[1] )
def controle_adequado_passivo( character ):
    character.modo_de_controle[2]( character )
def movimentacao_padrao( character, atividade:int ):
    (controle_adequado_passivo, controle_adequado_efetivo1, controle_adequado_efetivo2)[atividade](character)

root_funcoes =       [gravidade, rebate, colisao_com_plataformas, efeito_de_giro]
murasaki.funcoes +=  root_funcoes
drexa.funcoes +=     root_funcoes
arquimago.funcoes += [gravidade, colisao_com_plataformas]
cyber.funcoes +=     root_funcoes
maguinho.funcoes +=  [gravidade, colisao_com_plataformas]
logan.funcoes +=     root_funcoes


indice_player = 0
tempo_de_atraso_para_alternancia = 200
temporizador_de_atraso_de_alternancia = pygame.time.Clock()

def alternancia_personagem():
    global indice_player
    global tempo_de_atraso_para_alternancia

    temporizador_de_atraso_de_alternancia.tick()
    if tempo_de_atraso_para_alternancia > 0:
        tempo_de_atraso_para_alternancia -= temporizador_de_atraso_de_alternancia.get_time()
    else:    
        if pygame.key.get_pressed()[pygame.K_RETURN]:
            indice_player += 1
            if indice_player >= len(objetos.personagens):
                indice_player = 0
            tempo_de_atraso_para_alternancia = 200
    if indice_player >= len(objetos.personagens):
        indice_player = len(objetos.personagens)-1

def gambiarra_espada():
    if pygame.key.get_pressed()[K_SPACE]:
        objetos.swmmon_espada_voadora(
            player.rect.center,
            (
                {1: -10, 0:10}[player.left]+player.fisica.velocidade_lateral,
                #(cs(8, player.fisica.velocidade_lateral)+player.fisica.velocidade_lateral, 0)[int(player.fisica.velocidade_lateral==0)],
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

def get_rel_char(char):
    return (pre_tela_rect.centerx - char.rect.centerx, pre_tela_rect.centery - char.rect.centery)

def main():

    global indice_player
    global player

    pygame.time.Clock().tick(40)#40)

    alternancia_personagem()
    gambiarra_espada()

    player = objetos.personagens[ indice_player ]
    #player2 = objetos.personagens[ indice_player-1 ]

    for character in objetos.personagens:
        movimentacao_padrao(character, int(character==player)) #+2*int(character==player2))

    for i in objetos.fantasminhas + objetos.personagens:
        i.current_animation.run()#i.fisica.velocidade_lateral )
        i.run()

    rel_p1 = (get_rel_char(player ))#[0]-pre_size[0]/4, get_rel_char(player )[1])
    #rel_p2 = (get_rel_char(player2)[0]-pre_size[0]/4, get_rel_char(player2)[1])

    for i in objetos.fantasminhas + objetos.personagens:
        renderiza_personagem( i, pre_tela, rel_p1 )
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

    remove_personagem(indice_player)

    for i in range(len(tileset_array)):
        renderiza_quadrados( tileset_array[i][1], pre_tela, rel_p1 )
    #    renderiza_tilesetpack( tileset_array[i], pre_tela, rel_p1, tamanho_dos_tiles )

    desenha_coracoes()
    renderiza_tela()
