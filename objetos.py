from personagem import personagens as lista_personagens, monstrinho
import tileset
import efeitos_visuais

personagens = lista_personagens
fantasminhas = [ monstrinho ]
particulas = []
plataformas = tileset.plataformas

def adiciona_particula( nome , posicao ):
    caminho = efeitos_visuais.animacoes[ nome ]
    a = efeitos_visuais.ObjetoEfemero( posicao, caminho )
    particulas.append( a )

def adiciona_bandeira( posicao ):
    particulas.append( efeitos_visuais.BandeiraDerrota( posicao ) )