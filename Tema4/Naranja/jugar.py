import json
from pathlib import Path

BASE_DIR = Path.cwd()
DATA_DIR = BASE_DIR / "data"
ARCHIVO_MATRIZ = DATA_DIR / "matriz.json"

COLORES = ["rojo", "azul", "verde", "amarillo", "naranja", "morado"]


def cargar_matriz():
    with open(ARCHIVO_MATRIZ, "r", encoding="utf-8") as archivo:
        return json.load(archivo)


def inundar(matriz, nuevo_color):
    # Simula la expansión desde (0,0)

    filas = len(matriz)
    columnas = len(matriz[0])
    color_inicial = matriz[0][0]

    if nuevo_color == color_inicial:
        return 0

    visitado = []             
    pila = [(0, 0)]
    visitado.append((0, 0))

    zona_original = []

    # Encuentra la zona del color original
    while pila:
        x, y = pila.pop()
        zona_original.append((x, y))

        for mov_x, mov_y in [(1,0), (-1,0), (0,1), (0,-1)]:
            nx = x + mov_x
            ny = y + mov_y

            if 0 <= nx < filas and 0 <= ny < columnas:
                if matriz[nx][ny] == color_inicial:
                    if (nx, ny) not in visitado:
                        visitado.append((nx, ny))
                        pila.append((nx, ny))

    # Expansión con el nuevo color
    nueva_zona = zona_original.copy()
    pila2 = zona_original.copy()

    while pila2:
        x, y = pila2.pop()

        for mov_x, mov_y in [(1,0), (-1,0), (0,1), (0,-1)]:
            nx = x + mov_x
            ny = y + mov_y

            if 0 <= nx < filas and 0 <= ny < columnas:
                if matriz[nx][ny] == nuevo_color:
                    if (nx, ny) not in nueva_zona:
                        nueva_zona.append((nx, ny))
                        pila2.append((nx, ny))

    return len(nueva_zona)


def mejor_color(matriz):
    # Devuelve el color que produce la expansión más grande
    mejor = None
    mayor_tamano = -1

    for color in COLORES:
        tamano = inundar(matriz, color)
        if tamano > mayor_tamano:
            mayor_tamano = tamano
            mejor = color

    return mejor


def main():
    matriz = cargar_matriz()
    print("Mejor color:", mejor_color(matriz))


if __name__ == "__main__":
    main()
