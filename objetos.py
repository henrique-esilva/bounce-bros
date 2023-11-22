from personagem import personagens as lista_personagens, monstrinho, boca
from tileset import plataformas
import efeitos_visuais

personagens = lista_personagens
fantasminhas = [ monstrinho, boca ]
particulas = []
plataformas = plataformas

def adiciona_particula( nome , posicao ):
    caminho = efeitos_visuais.animacoes[ nome ]
    a = efeitos_visuais.ObjetoEfemero( posicao , caminho )
    particulas.append( a )

def adiciona_bandeira( posicao ):
    particulas.append( efeitos_visuais.BandeiraDerrota( posicao ) )