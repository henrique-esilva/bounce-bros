from personagem import murasaki, drexa, monstrinho
import tileset
import efeitos_visuais

personagens = [ drexa, murasaki ]
fantasminhas = [ monstrinho ]
particulas = []
plataformas = tileset.plataformas

def adiciona_particula( nome , posicao ):
    caminho = efeitos_visuais.animacoes[ nome ]
    a = efeitos_visuais.ObjetoEfemero( posicao, caminho )
    particulas.append( a )