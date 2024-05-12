import personagem as pers
from tileset import plataformas
import efeitos_visuais
from copy import copy

from obj_moveis import EspadaVoadora

personagens_originais = [pers.murasaki, pers.drexa, pers.arquimago, pers.cyber, pers.maguinho, pers.logan, pers.mandy]
fantasminhas_originais = [ pers.monstrinho, pers.boca, pers.monstrinho2 ]

murasaki  = pers.create_murasaki()
drexa     = pers.create_drexa()
arquimago = pers.create_arquimago()
cyber     = pers.create_cyber()
maguinho  = pers.create_maguinho()
logan     = pers.create_logan()
mandy     = pers.create_mandy()

monstrinho  = pers.create_monstrinho()
boca        = pers.create_boca()
monstrinho2 = pers.create_monstrinho2()

personagens = [murasaki, drexa, arquimago, cyber, maguinho, logan, mandy]
fantasminhas = [ monstrinho, boca, monstrinho2 ]
particulas = []
obj_moveis = []
plataformas = plataformas

def swmmon_espada_voadora(pos, vel, comportamento, left):
    a = EspadaVoadora(left)
    a.rect.center = pos
    a.fisica.velocidade_lateral  = vel[0]
    a.fisica.velocidade_de_queda = vel[1]
    a.fisica.coeficiente_de_rotacao = 2
    a.comportamento.extend(comportamento)
    a.ref = obj_moveis
    obj_moveis.append(a)

def adiciona_particula( nome , posicao ):
    caminho = efeitos_visuais.animacoes[ nome ]
    a = efeitos_visuais.ObjetoEfemero( posicao , caminho )
    particulas.append( a )

def adiciona_bandeira( posicao ):
    particulas.append( efeitos_visuais.BandeiraDerrota( posicao ) )