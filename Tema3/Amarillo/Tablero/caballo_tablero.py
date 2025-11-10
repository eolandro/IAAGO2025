N = 8

movimientosX = [2, 1, -1, -2, -2, -1, 1, 2]
movimientosY = [1, 2, 2, 1, -1, -2, -2, -1]

def imprimir_tablero(tablero):
    for fila in tablero:
        print(fila)

def es_valido(x, y, tablero):
    return x >= 0 and y >= 0 and x < N and y < N and tablero[x][y] == "~" 

def contar_movimientos(x, y, tablero):
    cuenta = 0
    for i in range(8):
        nuevoX = x + movimientosX[i]
        nuevoY = y + movimientosY[i]
        if es_valido(nuevoX, nuevoY, tablero):
            cuenta += 1
    return cuenta

def siguiente_movimiento(x, y, tablero):
    min_grado = 9
    mejor_movimiento = (-1, -1)

    for i in range(8):
        nuevoX = x + movimientosX[i]
        nuevoY = y + movimientosY[i]
        if es_valido(nuevoX, nuevoY, tablero):
            grado = contar_movimientos(nuevoX, nuevoY, tablero)
            if grado < min_grado:
                min_grado = grado
                mejor_movimiento = (nuevoX, nuevoY)

    return mejor_movimiento

def resolver_caballo(x, y):
    tablero = [["~" for _ in range(N)] for _ in range(N)]
    x_inicial, y_inicial = x, y

    tablero[x_inicial][y_inicial] = 0

    x, y = x_inicial, y_inicial

    for movimiento_actual in range(1, N * N):
        siguiente = siguiente_movimiento(x, y, tablero)
        if siguiente == (-1, -1):
            print("No existe una solución")
            return False
        x, y = siguiente
        print(f"{movimiento_actual}° Movimiento")
        print("\n")
        tablero[x][y] = movimiento_actual
        imprimir_tablero(tablero)
        print("\n")
    return True
print("--------------Caballo en el tablero-------------- ")


corde = input('Elige la posición con la que quieres comenzar :) (ejemplo 0,0): ')
print()
fila, col = map(int, corde.split(','))
resolver_caballo(fila, col)
