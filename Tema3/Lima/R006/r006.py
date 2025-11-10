def crearTablero(t):
    return [[-1 for i in range (t)] for j in range (t)]

def movimiento(tablero, x, y):
    t = len(tablero)
    return (0 <= x < t) and (0 <= y < t) and (tablero[x][y] == -1)

def backtracking(tablero, x, y, i):
    t = len(tablero)
    if i == t * t:
        return True
                #x,y    #x,y    #-x,y    #-x,y    #-x,-y    #-x,-y    #x,-y    #x,-y
    caballo = [(2, 1), (1, 2), (-1, 2), (-2, 1), (-2, -1), (-1, -2), (1, -2), (2, -1)]

    for ix, iy in caballo:
        ax, by = x + ix, y + iy
        if movimiento(tablero, ax, by):
            tablero[ax][by] = i
            if backtracking(tablero, ax, by, i+1):
                return True
            tablero[ax][by] = -1
    return False

def imprimir(tablero):
    t = len(tablero)
    for i in range(t):
        for j in range(t):
            #print()
            print(f"{tablero[i][j]:2}", end=" ")
        print()


t=8

tablero=crearTablero(t)
#imprimir(tablero)
x=0
y=0
tablero[x][y]=0
#imprimir(tablero)
#"""
if backtracking(tablero, x, y, 1):
    imprimir(tablero)
else:
    print("Error")
#"""
