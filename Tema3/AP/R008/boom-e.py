import heapq
import yaml

with open("config_boom.yaml", "r") as f:
    config = yaml.safe_load(f)

mapa = config['mapa']

#A*
def heuristica(a, b):
    """Distancia Manhattan"""
    return abs(a[0] - b[0]) + abs(a[1] - b[1])

def vecinos_validos(mapa, nodo):
    """Devuelve vecinos válidos (no obstáculos)"""
    fila, col = nodo
    posibles = [(fila-1,col),(fila+1,col),(fila,col-1),(fila,col+1)]
    vecinos = []
    for r,c in posibles:
        if 0 <= r < len(mapa) and 0 <= c < len(mapa[0]):
            if mapa[r][c] != 1:
                vecinos.append((r,c))
    return vecinos

def a_star(mapa, inicio, objetivo):
    """Implementación de A*"""
    abierto = []
    heapq.heappush(abierto, (0 + heuristica(inicio, objetivo), 0, inicio))
    came_from = {}
    g_score = {inicio: 0}

    while abierto:
        _, costo_actual, nodo_actual = heapq.heappop(abierto)

        if nodo_actual == objetivo:
            # Reconstruir ruta
            ruta = []
            while nodo_actual in came_from:
                ruta.append(nodo_actual)
                nodo_actual = came_from[nodo_actual]
            ruta.append(inicio)
            ruta.reverse()
            return ruta

        for vecino in vecinos_validos(mapa, nodo_actual):
            tentative_g = costo_actual + 1
            if vecino not in g_score or tentative_g < g_score[vecino]:
                g_score[vecino] = tentative_g
                f = tentative_g + heuristica(vecino, objetivo)
                heapq.heappush(abierto, (f, tentative_g, vecino))
                came_from[vecino] = nodo_actual

    return None


bomba_pos = None
for r in range(len(mapa)):
    for c in range(len(mapa[0])):
        if mapa[r][c] == 2:
            bomba_pos = (r, c)
            break
    if bomba_pos: break

inicio = (0,0)  # inicio del pathfinding
if not bomba_pos:
    print("No se encontró la bomba en el mapa.")
    exit()

ruta = a_star(mapa, inicio, bomba_pos)


def mostrar_ruta_tablero(mapa, ruta):
    mapa_visual = [fila[:] for fila in mapa]
    for r,c in ruta:
        if mapa_visual[r][c] == 0:
            mapa_visual[r][c] = '*'
        elif mapa_visual[r][c] == 2:
            mapa_visual[r][c] = 'B'

    for fila in mapa_visual:
        fila_str = ""
        for celda in fila:
            if celda == 1:
                fila_str += " # "
            elif celda == '*':
                fila_str += " * "
            elif celda == 'B':
                fila_str += " B "
            else:
                fila_str += " . "
        print(fila_str)

if ruta:
    print("Ruta encontrada usando A*:\n")
    print(ruta)
    print("\nTablero con ruta:")
    mostrar_ruta_tablero(mapa, ruta)
else:
    print("No se encontró ruta.")
