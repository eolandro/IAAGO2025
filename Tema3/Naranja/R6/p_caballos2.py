
# Función para verificar si un movimiento es válido
def es_valido(x, y, tablero):
    if x >= 0 and x < 8 and y >= 0 and y < 8 and tablero[x][y] == 0:
        return True
    else:
        return False

# Función principal que calcula el recorrido
def recorrido_caballo(x_inicial, y_inicial):
    # Movimientos posibles del caballo
    movimientos = [
        (2, 1), (1, 2), (-1, 2), (-2, 1),
        (-2, -1), (-1, -2), (1, -2), (2, -1)
    ]

    # Crear el tablero de 8x8 con ceros
    tablero = []
    for i in range(8):
        fila = []
        for j in range(8):
            fila.append(0)
        tablero.append(fila)

    # Marcar la posición inicial
    tablero[x_inicial][y_inicial] = 1

    # Posición actual
    x = x_inicial
    y = y_inicial

    # Función interna para contar los movimientos posibles desde una casilla
    def contar_movimientos(x, y):
        contador = 0
        for mov in movimientos:
            nx = x + mov[0]
            ny = y + mov[1]
            if es_valido(nx, ny, tablero):
                contador += 1
        return contador

    # Repetir hasta llenar las 64 casillas
    for paso in range(2, 65):
        siguiente_x = -1
        siguiente_y = -1
        menor_grado = 9  # máximo posible de movimientos es 8

        # Buscar entre los movimientos posibles el que tenga menos opciones futuras
        for mov in movimientos:
            nx = x + mov[0]
            ny = y + mov[1]
            if es_valido(nx, ny, tablero):
                grado = contar_movimientos(nx, ny)
                if grado < menor_grado:
                    menor_grado = grado
                    siguiente_x = nx
                    siguiente_y = ny

        # Si no hay movimientos válidos, el recorrido falla
        if siguiente_x == -1 and siguiente_y == -1:
            print("No se pudo completar el recorrido.")
            return tablero, False

        # Avanzar al siguiente paso
        x = siguiente_x
        y = siguiente_y
        tablero[x][y] = paso

    print("Recorrido completado con éxito.\n")
    return tablero, True

# Función para imprimir el tablero en formato bonito
def imprimir_tablero(tablero):
    for fila in tablero:
        for valor in fila:
            print(f"{valor:2d}", end=" ")
        print()
    print()


print("\n=== MÉTODO HEURÍSTICO: ALGORITMO DE WARNSDORFF ===")
print("Este método usa una regla inteligente que elige siempre la casilla")
print("con menos opciones futuras para evitar quedar atrapado.\n")

fila = int(input("Ingresa la fila inicial (0-7): "))
columna = int(input("Ingresa la columna inicial (0-7): "))
print()

tablero, exito = recorrido_caballo(fila, columna)
imprimir_tablero(tablero)
