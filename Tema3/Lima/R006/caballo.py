N = 8

movimientos_x = [2, 1, -1, -2, -2, -1, 1, 2]
movimientos_y = [1, 2, 2, 1, -1, -2, -2, -1]

def es_valido(x, y, tablero):
    if x < 0:
        return False
    if x >= N:
        return False

    if y < 0:
        return False
    if y >= N:
        return False

    if tablero[x][y] != -1:
        return False

    return True


def resolver_caballo(tablero, x, y, mov_contador):
    """Función recursiva para recorrer el tablero."""

    if mov_contador == N * N:
        return True

    # Prueba los posibles movimientos
    for i in range(8):
        sig_x = x + movimientos_x[i]
        sig_y = y + movimientos_y[i]
        if es_valido(sig_x, sig_y, tablero):
            tablero[sig_x][sig_y] = mov_contador
            if resolver_caballo(tablero, sig_x, sig_y, mov_contador + 1):
                return True
            # Backtracking
            tablero[sig_x][sig_y] = -1
    return False

def imprimir_tablero(tablero):
    for fila in tablero:
        print(' '.join(f'{celda:2}' for celda in fila))
    print()

def recorrido_caballo():
    """Pide coordenadas, inicializa el tablero y resuelve el recorrido."""
    while True:
        try:
            pos_x = int(input("Ingresa la coordenada X (0-7): "))
            pos_y = int(input("Ingresa la coordenada Y (0-7): "))
            if 0 <= pos_x < N and 0 <= pos_y < N:
                break
            else:
                print("Coordenadas fuera del rango. Intenta de nuevo.")
        except ValueError:
            print("Por favor ingresa un número válido.")

    # Crear tablero vacío
    tablero = [[-1 for _ in range(N)] for _ in range(N)]
    tablero[pos_x][pos_y] = 0  

    if not resolver_caballo(tablero, pos_x, pos_y, 1):
        print("No existe solución desde esa posición.")
    else:
        imprimir_tablero(tablero)

# Ejecutar
recorrido_caballo()

