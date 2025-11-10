def rotar(matriz, rotaciones, historial):
    copia = []
    for fila in matriz:
        copia.append(fila[:])
    historial.append(copia)

    if rotaciones == 0:
        return historial

    n = len(matriz)
    borde = []


    for j in range(n):
        borde.append(matriz[0][j])
    for i in range(1, n - 1):
        borde.append(matriz[i][n - 1])
    for j in range(n - 1, -1, -1):
        borde.append(matriz[n - 1][j])
    for i in range(n - 2, 0, -1):
        borde.append(matriz[i][0])

    nueva_posicion = borde[-3:] + borde[:-3]

    k = 0
    for j in range(n):
        matriz[0][j] = nueva_posicion[k]
        k += 1
    for i in range(1, n - 1):
        matriz[i][n - 1] = nueva_posicion[k]
        k += 1
    for j in range(n - 1, -1, -1):
        matriz[n - 1][j] = nueva_posicion[k]
        k += 1
    for i in range(n - 2, 0, -1):
        matriz[i][0] = nueva_posicion[k]
        k += 1
        
    return rotar(matriz, rotaciones - 1, historial)

tablero = [['~', '~', '~'],
           ['~', '~', '~'],
           ['~', '~', '~']]

tablero[0][0] = 'CN'  # Caballo negro
tablero[0][2] = 'CN'
tablero[2][0] = 'CB'  # Caballo blanco
tablero[2][2] = 'CB'

veces = 4

resultado = rotar(tablero, veces, [])

for n, estado in enumerate(resultado):
    print(f"Rotación {n}:")
    for fila in estado:
        print(fila)
    print()