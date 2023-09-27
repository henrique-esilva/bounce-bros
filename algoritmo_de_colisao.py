def intervalo_retroativo( rect, velocidade, direcao ):
    conjunto = [
        [rect.left, rect.right ],
        [rect.top,  rect.bottom],
    ][direcao]
    #define cálculo
    base = conjunto[int(velocidade<0)]
    return (base, base-velocidade)