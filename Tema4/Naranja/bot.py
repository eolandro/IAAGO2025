import time
from pathlib import Path
import pyautogui

from analizar import analizar_tablero
from jugar import mejor_color

BASE_DIR = Path.cwd()
DATA_DIR = BASE_DIR / "data"
ARCHIVO_CONFIG = DATA_DIR / "open_flood_config.json"
ARCHIVO_MATRIZ = DATA_DIR / "matriz.json"


def cargar_configuracion():
    import json
    with open(ARCHIVO_CONFIG, "r", encoding="utf-8") as archivo:
        return json.load(archivo)


def capturar_tablero(region):
    imagen = pyautogui.screenshot(
        region=(region["x"], region["y"], region["ancho"], region["alto"])
    )
    imagen.save(DATA_DIR / "tablero.png")


def hacer_click(config, color):
    x = config["botones"][color]["x"]
    y = config["botones"][color]["y"]
    pyautogui.click(x, y)


def detectar_popup(config):
    x = config["popup"]["x"]
    y = config["popup"]["y"]

    r, g, b = pyautogui.screenshot().getpixel((x, y))
    es_blanco = (r > 220) and (g > 220) and (b > 220)
    return es_blanco


def tablero_cambiado(matriz1, matriz2):
    return matriz1 != matriz2


def main():
    print("\nBot iniciado...\n")

    config = cargar_configuracion()
    region = config["tablero"]

    # SIEMPRE genera la matriz inicial
    print("Generando matriz inicial...")
    capturar_tablero(region)
    analizar_tablero()
    print("Matriz inicial generada.\n")

    while True:

        if detectar_popup(config):
            print("Popup detectado. Bot detenido.")
            break

        # Analiza tablero actual
        capturar_tablero(region)
        matriz = analizar_tablero()

        # Mejor color
        color = mejor_color(matriz)
        print("Color elegido:", color)

        # Copia real del tablero
        matriz_antes = [fila[:] for fila in matriz]

        # Clic
        hacer_click(config, color)
        time.sleep(0.5)

        # Analiza de nuevo
        capturar_tablero(region)
        matriz_despues = analizar_tablero()

        # Si no cambió, evita repetir el color
        if not tablero_cambiado(matriz_antes, matriz_despues):
            print("El tablero no cambió. Buscando nuevo color...")
            continue

    print("\nBot finalizado.\n")


main()
