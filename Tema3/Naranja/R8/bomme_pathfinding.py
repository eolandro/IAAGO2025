import random
from ruamel.yaml import YAML

# ---- FUNCIONES BÁSICAS ----

def buscar_posicion(tablero, elemento):
    for i in range(len(tablero)):
        for j in range(len(tablero[0])):
            if tablero[i][j] == elemento:
                return (i, j)
    return None

def es_valida(tablero, pos):
    i, j = pos
    return 0 <= i < len(tablero) and 0 <= j < len(tablero[0]) and tablero[i][j] != 'X'


def obtener_vecinos(tablero, pos):
    i, j = pos
    vecinos = []

    # Movimientos ortogonales (costo 1)
    for di, dj in [(-1,0), (1,0), (0,-1), (0,1)]:
        nueva_pos = (i + di, j + dj)
        if es_valida(tablero, nueva_pos):
            vecinos.append((nueva_pos, 1))

    # Movimientos diagonales (costo 2)
    for di, dj in [(-1,-1), (-1,1), (1,-1), (1,1)]:
        nueva_pos = (i + di, j + dj)
        if es_valida(tablero, nueva_pos):
            vecinos.append((nueva_pos, 2))
    
    return vecinos


def calcular_distancia(pos1, pos2):
    i1, j1 = pos1
    i2, j2 = pos2
    return abs(i1 - i2) + abs(j1 - j2)


def encontrar_camino(tablero, boome_pos, bomba_pos):
    casillas_exploradas = [boome_pos]
    print(f"Boome inicia en: {boome_pos}")
    print(f"Bomba en: {bomba_pos}\n")

    pos_actual = boome_pos

    while pos_actual != bomba_pos:
        vecinos = obtener_vecinos(tablero, pos_actual)
        if not vecinos:
            print("¡No hay camino posible!")
            return None, None

        mejores_vecinos = []
        menor_valor = None

        for vecino, costo in vecinos:
            if vecino in casillas_exploradas:
                continue

            distancia_a_bomba = calcular_distancia(vecino, bomba_pos)
            heuristica = costo + distancia_a_bomba

            if menor_valor is None or heuristica < menor_valor:
                menor_valor = heuristica
                mejores_vecinos = [vecino]
            elif heuristica == menor_valor:
                mejores_vecinos.append(vecino)

        if not mejores_vecinos:
            print("¡No se puede avanzar más!")
            return None, None

        siguiente_pos = random.choice(mejores_vecinos)
        pos_actual = siguiente_pos
        casillas_exploradas.append(pos_actual)
        print(f"Boome se mueve a: {pos_actual}")

    print("¡Boome ha llegado a la bomba!")
    camino_final = encontrar_camino_rapido(tablero, boome_pos, bomba_pos, casillas_exploradas)
    return casillas_exploradas, camino_final


def encontrar_camino_rapido(tablero, boome_pos, bomba_pos, casillas_exploradas):
    camino = [bomba_pos]
    pos_actual = bomba_pos

    while pos_actual != boome_pos:
        todos_los_vecinos = obtener_vecinos(tablero, pos_actual)

        vecinos_validos = []
        for vecino_info in todos_los_vecinos:
            vecino = vecino_info[0]
            if vecino in casillas_exploradas and vecino not in camino:
                vecinos_validos.append(vecino)

        if not vecinos_validos:
            break

        vecino_mas_cercano = None
        menor_distancia = None
        for vecino in vecinos_validos:
            distancia = calcular_distancia(vecino, boome_pos)
            if menor_distancia is None or distancia < menor_distancia:
                menor_distancia = distancia
                vecino_mas_cercano = vecino

        if vecino_mas_cercano:
            camino.append(vecino_mas_cercano)
            pos_actual = vecino_mas_cercano
        else:
            break

    return camino[::-1]


def mostrar_resultado(camino_final):
    print("\nRESULTADO FINAL")
    print(f"\nCamino más rápido ({len(camino_final)} pasos):")
    for paso in camino_final:
        print(paso)


# ---- FUNCIÓN PRINCIPAL ----

def main():
    yaml = YAML()
    with open('tablero.yaml', 'r', encoding='utf-8') as archivo:
        datos = yaml.load(archivo)

    tablero = datos['tablero']

    print("TABLERO INICIAL:")
    for fila in tablero:
        print("  " + " ".join(fila))
    print()

    boome_pos = buscar_posicion(tablero, 'B')
    bomba_pos = buscar_posicion(tablero, 'P')

    casillas_exploradas, camino_final = encontrar_camino(tablero, boome_pos, bomba_pos)

    if camino_final:
        mostrar_resultado(camino_final)
    else:
        print("No se pudo encontrar un camino hasta la bomba.")


# Ejecutar el programa
main()
