from personagem import murasaki, drexa, arquimago, cyber, maguinho
from renderiza import *
from moving_functions import *

import objetos

objetos.monstrinho.funcoes.append( movimentacao_automatica_cossenoidal )
objetos.monstrinho.funcoes.append( movimentacao_automatica_senoidal )

imagem_coracao = pygame.image.load( "efeitos\\coracao.png" )

murasaki.funcoes =  [gravidade, rebate, colisao_com_plataformas, efeito_de_giro]
drexa.funcoes =     [gravidade, rebate, colisao_com_plataformas, efeito_de_giro]
arquimago.funcoes = [gravidade, colisao_com_plataformas]
cyber.funcoes =     [gravidade, rebate, colisao_com_plataformas, efeito_de_giro]
maguinho.funcoes =  [gravidade, colisao_com_plataformas]

murasaki.modo_de_controle = ( controle_lateral_pula, 10 )
drexa.modo_de_controle = ( controle_lateral_pula, 10 )
arquimago.modo_de_controle = ( controle_voo, 8 )
cyber.modo_de_controle = ( controle_lateral_pula, 8 )
maguinho.modo_de_controle = ( controle_voo, 8 )

    # salto base
    # mulplicador de velocidade
murasaki.multiplicadores_de_salto = (-28, 1  )
drexa.   multiplicadores_de_salto = (-30, 1.5)
cyber.   multiplicadores_de_salto = (-30, 0  )

    # velocidade minima de ativação
    # multiplicador de velocidade adicional
murasaki.multiplicadores_de_velocidade = (12, {False: 1, True:2  })
drexa.   multiplicadores_de_velocidade = (12, {False: 1, True:1  })
cyber.   multiplicadores_de_velocidade = (16, {False: 1, True:1  })

indice_player = 0
tempo_de_atraso_para_alternancia = 200
temporizador_de_atraso_de_alternancia = pygame.time.Clock()

def alterna_personagem():
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

def remove_personagem():
    global indice_player
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

    pygame.time.Clock().tick(40)

    alterna_personagem()

    player = objetos.personagens[ indice_player ]
    player2 = objetos.personagens[ indice_player-1 ]

    rel_p1 = (get_rel_char(player )[0]-pre_size[0]/4, get_rel_char(player )[1])
    rel_p2 = (get_rel_char(player2)[0]-pre_size[0]/4, get_rel_char(player2)[1])

    for character in objetos.personagens:
        if character == player:
            character.modo_de_controle[0]( character, 0, character.modo_de_controle[1] )
        elif character == player2:
            character.modo_de_controle[0]( character, 1, character.modo_de_controle[1] )
        elif character.modo_de_controle[0] != controle_voo:
            desacelera_move_lateral_ajusta( character )
        else:
            desaceleracao_aerea( character )

    for i in objetos.particulas:

        if not i.current_animation.rodando:
            objetos.particulas.remove(i)

        i.current_animation.run()
        renderiza_particula( i, pre_tela, rel_p1 )
        renderiza_particula( i, mini_tela, rel_p2 )

    for i in objetos.fantasminhas:
        i.run()
        i.current_animation.run()# i.fisica.velocidade_lateral )
        renderiza_personagem( i, pre_tela, rel_p1 )
        renderiza_personagem( i, mini_tela, rel_p2 )

    for i in objetos.personagens:
        i.current_animation.run()# i.fisica.velocidade_lateral )
        i.run()
        renderiza_personagem( i, pre_tela, rel_p1 )
        renderiza_personagem( i, mini_tela, rel_p2 )

    remove_personagem()

    renderiza_tiles( objetos.plataformas, pre_tela, rel_p1 )
    renderiza_tiles( objetos.plataformas, mini_tela, rel_p2 )
    desenha_coracoes()
    renderiza_tela()