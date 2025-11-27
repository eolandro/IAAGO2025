from PIL import Image
import json
from pathlib import Path

BASE_DIR = Path.cwd()
DATA_DIR = BASE_DIR / "data"
IMG_TABLERO = DATA_DIR / "tablero.png"
ARCHIVO_MATRIZ = DATA_DIR / "matriz.json"

TAM_TABLERO = 18

COLORES_REFERENCIA = {
    "rojo":     (230, 63, 54),
    "azul":     (104, 143, 232),
    "verde":    (78, 162, 74),
    "amarillo": (255, 211, 78),
    "naranja":  (255, 138, 56),
    "morado":   (153, 102, 204),
}

def diferencia_color(c1, c2):
    # Calcula la diferencia entre dos colores RGB
    r = c1[0] - c2[0]
    g = c1[1] - c2[1]
    b = c1[2] - c2[2]

    distancia = (r * r + g * g + b * b) ** 0.5
    return distancia


def color_cercano(pixel):
    # Toma el primer color como mejor color inicial
    lista = list(COLORES_REFERENCIA.items())
    mejor_color, mejor_rgb = lista[0]
    mejor_dist = diferencia_color(pixel, mejor_rgb)

    # Compara contra el resto de colores
    for nombre, ref in lista[1:]:
        d = diferencia_color(pixel, ref)
        if d < mejor_dist:
            mejor_color = nombre
            mejor_dist = d

    return mejor_color

def analizar_tablero():
    # Carga la imagen recortada del tablero
    imagen = Image.open(IMG_TABLERO)
    ancho, alto = imagen.size

    # Calcula tamaño de cada celda
    celda_w = ancho / TAM_TABLERO
    celda_h = alto / TAM_TABLERO

    matriz = []

    # Recorre cada celda del tablero
    for fila in range(TAM_TABLERO):
        fila_colores = []

        for col in range(TAM_TABLERO):
            # Toma un pixel del centro de la celda
            px = int(col * celda_w + celda_w / 2)
            py = int(fila * celda_h + celda_h / 2)

            pixel = imagen.getpixel((px, py))[:3]

            # Encuentra el color más parecido al pixel
            color = color_cercano(pixel)

            fila_colores.append(color)

        matriz.append(fila_colores)

    # Guarda la matriz en un archivo JSON
    with open(ARCHIVO_MATRIZ, "w", encoding="utf-8") as archivo:
        json.dump(matriz, archivo, indent=4)

    return matriz
