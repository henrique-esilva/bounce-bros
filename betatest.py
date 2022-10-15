from personagem import murasaki, drexa, monstrinho, Personagem, Movimentacao_cossenoidal
from renderiza import *
from moving_functions import *

import objetos

imagem_coracao = pygame.image.load( "coracao.png" )




def desenha_coracoes():
    y = 0
    for i in objetos.personagens:
        x = 0
        for vida in range(i.vidas):
            #desenhar um coração vermelho
            pre_tela.blit( imagem_coracao, pygame.Rect( 5 + x * 16, 5 + y * 24, 0, 0 ) )
            x += 1
        y += 1

def remove_personagem():
    y = 0
    for i in objetos.personagens:
        for inimigo in objetos.fantasminhas:
            if i.fisica.retangulo_do_corpo.colliderect( inimigo.fisica.retangulo_do_corpo ):
                pass
                #i.vidas = 0
        if i.vidas == 0:
            objetos.personagens.pop( y )
        y += 1

def main():

    pygame.time.Clock().tick(40)

    for i in objetos.particulas:
        i.current_animation.run()
        renderiza_particula( i )

    for i in objetos.fantasminhas:
        i.current_animation.run()
        i.run()
        gravidade( i )
        renderiza_personagem( i )
        movimentacao_automatica_cossenoidal( i )

    for i in objetos.personagens:
        i.current_animation.run()
        i.run()
        gravidade( i )
        efeito_de_giro( i )
        colisao_com_plataformas( i , objetos.plataformas )
        #print( is_landed( i ) )
        rebate( i )
        renderiza_personagem( i )

    if murasaki.vidas:
        controle_lateral_pula(murasaki, 0)
    if drexa.vidas:
        controle_lateral_pula(drexa, 1)

    renderiza_tiles( objetos.plataformas )
    desenha_coracoes()
    remove_personagem()
    renderiza_tela()