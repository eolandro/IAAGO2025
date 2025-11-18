tablero=[
    ['C', ' ', 'C'],
    [' ',  ' ', ' ' ],
    ['c', ' ', 'c']
]

resp=[
    ['c', ' ', 'c'],
    [' ',  ' ', ' ' ],
    ['C', ' ', 'C']
]

caballos = ['Cn2', 'Cb2', 'Cb1', 'Cn1']

movs=[(2,1),(1,2),(-1,2),(-2,1),(-2,-1),(-1,-2),(1,-2),(2,-1)]

def imprimir():
    for fila in tablero:
        print(fila)
    print("--------------------------")

pos={'Cn1':(0,0), 'Cn2':(0,2), 'Cb1':(2,0), 'Cb2':(2,2)}

def movimiento(caballo):
    x,y = pos[caballo]
    for ix, iy in movs:
        ax, by = x + ix, y + iy
        if 0 <= ax < 3 and 0 <= by < 3 and tablero[ax][by] == ' ':
            tablero[x][y] = ' '
            if caballo=='Cb1' or caballo=='Cb2':
                tablero[ax][by] = 'c'
            else:
                tablero[ax][by] = 'C'
            pos[caballo] = (ax,by)
            imprimir()
            return True
    return False

r = False
while not r:
    for caballo in caballos:
        movimiento(caballo)
        if tablero == resp:
            r = True
            break

print("---------Fin-----------------")
