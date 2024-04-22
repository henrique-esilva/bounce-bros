from personagem import personagens as lista_personagens, monstrinho, monstrinho2, boca
from tileset import plataformas
import efeitos_visuais

from obj_moveis import EspadaVoadora


personagens = lista_personagens
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