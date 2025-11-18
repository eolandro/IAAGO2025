movs = [[(2,4),(3,6)],[(4,7),(5,9)],[(5,8),(6,10)],
        [(2,1),(5,6),(7,11),(8,13)],[(8,12),(9,14)],
        [(3,1),(5,4),(9,13),(10,15)],[(4,2),(8,9)],
        [(5,3),(9,10)],[(5,2),(8,7)],[(6,3),(9,8)],[(7,4),(12,13)],
        [(8,5),(13,14)],[(8,4),(9,6),(12,11),(14,15)],[(9,5),(13,12)],[(10,6),(14,13)]]


def tablero():
    tablero=[]
    c=0
    for fila in range(5):
        tablero.append([])
        for columna in range(fila+1):
            tablero[fila].append(c)
            c+=1
    return tablero

def imprimir(tablero):
    for fila in tablero:
        print("{:^22}".format(str(fila)))

def juego(pin):
    tablero = []
    c=0
    for fila in range(5):
        tablero.append([])
        for columna in range(fila+1):
            if pin == c:
                tablero[fila].append(0)
            else:
                tablero[fila].append(1)
            c+=1
    return tablero

def peones(pin):
    pines = [1]*15
    pines[pin] = 0
    return pines

def movimiento(movs, inicio):
    p=peones(inicio)
    camino=backtracking(p, movs, [0]*13, 0)
    return camino

def backtracking(pines, movs, pila, cont):
    if sum(pines)==1:
        return pila
    movimientos=avanzar(pines.copy(), movs)
    for i in movimientos:
        pila[cont]=(i[0], i[2])
        camino=backtracking(modificar(pines.copy(), i),movs,pila,cont+1)
        if camino:
            return camino
    return False

def avanzar(pines, movs):
    movimientos=[]
    for fila in range(len(pines)):
        for columna in movs[fila]:
            if pines[fila] and pines[columna[0]-1] and not pines[columna[1]-1]:
                movimientos.append((fila, columna[0]-1, columna[1]-1))
    return movimientos

def modificar(pines, movimiento):
    pines[movimiento[0]]=0
    pines[movimiento[1]]=0
    pines[movimiento[2]]=1
    return pines

imprimir(tablero())
pin=int(input("Selecciona la pieza a retirar: "))
tab=juego(pin)
imprimir(tab)
r=movimiento(movs,pin)
print("-----------------Solucion-----------------")
print(r)


    



