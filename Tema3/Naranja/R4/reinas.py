# Crear un tablero vacío de 4x4
def crear_tablero():
    tablero = []
    for i in range(4):
        fila = [0, 0, 0, 0]
        tablero.append(fila)
    return tablero

# Marcar las posiciones atacadas por una reina
def bloquear(tablero, fila, col):
    n = 4

    # Fila y columna
    for j in range(n):
        tablero[fila][j] = 1
    for i in range(n):
        tablero[i][col] = 1

    # Diagonales
    i, j = fila, col
    while i >= 0 and j >= 0:
        tablero[i][j] = 1
        i -= 1
        j -= 1

    i, j = fila, col
    while i >= 0 and j < n:
        tablero[i][j] = 1
        i -= 1
        j += 1

    i, j = fila, col
    while i < n and j >= 0:
        tablero[i][j] = 1
        i += 1
        j -= 1

    i, j = fila, col
    while i < n and j < n:
        tablero[i][j] = 1
        i += 1
        j += 1

    # Marcar la reina con un 2
    tablero[fila][col] = 2

# Imprimir el tablero
def mostrar(tablero):
    for fila in tablero:
        linea = ""
        for celda in fila:
            if celda == 2:
                linea += "Q "
            elif celda == 1:
                linea += ". "
            else:
                linea += "X "
        print(linea)
    print()

# Programa principal
print("Resolviendo el problema de las 4 reinas en un tablero 4x4\n")

n = 4
soluciones = []

# Se prueban todas las combinaciones posibles
def colocar_reinas(fila, tablero):
    if fila == n:
        soluciones.append([fila[:] for fila in tablero])
        return

    for col in range(n):
        # Verificar si se puede colocar una reina aquí
        valido = True
        for i in range(fila):
            for j in range(n):
                if tablero[i][j] == 2:
                    if j == col or abs(i - fila) == abs(j - col):
                        valido = False
        if valido:
            nuevo = []
            for f in tablero:
                nuevo.append(f[:])
            nuevo[fila][col] = 2
            colocar_reinas(fila + 1, nuevo)

# Empezar desde la fila 0
tablero_inicial = crear_tablero()
colocar_reinas(0, tablero_inicial)

# Mostrar resultados
print("Se encontraron", len(soluciones), "soluciones:\n")
contador = 1
for sol in soluciones:
    print("Solución", contador)
    mostrar(sol)
    contador += 1
