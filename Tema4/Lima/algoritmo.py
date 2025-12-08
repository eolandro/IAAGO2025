# algoritmo.py
# Resuelve el tablero con estrategia greedy sencilla

def obtener_zona_inicial(matriz):
    filas = len(matriz)
    columnas = len(matriz[0])
    color_inicial = matriz[0][0]

    zona = set()
    zona.add((0, 0))
    cola = [(0, 0)]

    while cola:
        x, y = cola.pop(0)

        for dx, dy in [(1,0), (-1,0), (0,1), (0,-1)]:
            nx, ny = x + dx, y + dy

            if 0 <= nx < filas and 0 <= ny < columnas:
                if (nx, ny) not in zona and matriz[nx][ny] == color_inicial:
                    zona.add((nx, ny))
                    cola.append((nx, ny))

    return zona


def mejor_color(matriz, zona):
    contador = {}

    for (x, y) in zona:
        for dx, dy in [(1,0), (-1,0), (0,1), (0,-1)]:
            nx, ny = x + dx, y + dy

            if 0 <= nx < len(matriz) and 0 <= ny < len(matriz[0]):
                if (nx, ny) not in zona:
                    color = matriz[nx][ny]
                    contador[color] = contador.get(color, 0) + 1

    if not contador:
        return None

    return max(contador, key=contador.get)


def aplicar_color(matriz, zona, nuevo_color):
    for x, y in zona:
        matriz[x][y] = nuevo_color


def resolver_tablero(matriz, max_pasos=31):
    movimientos = []

    for _ in range(max_pasos):
        zona = obtener_zona_inicial(matriz)
        color = mejor_color(matriz, zona)

        if color is None:
            break

        aplicar_color(matriz, zona, color)
        movimientos.append(color)

    return movimientos
