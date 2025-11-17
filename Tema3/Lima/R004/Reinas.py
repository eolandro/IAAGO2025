import yaml

def es_posicion_segura(tablero, fila, columna):
    N = len(tablero)
    for i in range(fila):
        if tablero[i][columna] == 1:
            return False

    # Diagonal superior izquierda
    i, j = fila - 1, columna - 1
    while i >= 0 and j >= 0:
        if tablero[i][j] == 1:
            return False
        i -= 1
        j -= 1

    # Diagonal superior derecha
    i, j = fila - 1, columna + 1
    while i >= 0 and j < N:
        if tablero[i][j] == 1:
            return False
        i -= 1
        j += 1

    return True


def colocar_reinas(tablero, fila, soluciones):
    N = len(tablero)
    if fila == N:
        solucion = [fila[:] for fila in tablero]
        soluciones.append(solucion)
        return

    for columna in range(N):
        if es_posicion_segura(tablero, fila, columna):
            tablero[fila][columna] = 1
            colocar_reinas(tablero, fila + 1, soluciones)
            tablero[fila][columna] = 0


def cuatro_reinas():
    N = 4
    tablero = [[0] * N for _ in range(N)]
    soluciones = []
    colocar_reinas(tablero, 0, soluciones)
    return soluciones


# Generar y guardar soluciones
todas_las_soluciones = cuatro_reinas()
yaml_data = []

for indice, tablero in enumerate(todas_las_soluciones, start=1):
    # Convertimos cada fila en una cadena legible tipo "0 1 0 0"
    tablero_como_texto = [" ".join(str(x) for x in fila) for fila in tablero]

    solucion_yaml = {
        "solucion": indice,
        "tablero": tablero_como_texto
    }
    yaml_data.append(solucion_yaml)

# Guardar en YAML
with open("soluciones_4_reinas.yaml", "w") as archivo:
    yaml.dump(yaml_data, archivo, allow_unicode=True, sort_keys=False)

print(f"Se encontraron {len(todas_las_soluciones)} soluciones.")
