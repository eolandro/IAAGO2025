import json
import time
from pathlib import Path
import pyautogui

BASE_DIR = Path.cwd()
DATA_DIR = BASE_DIR / "data"
ARCHIVO_CONFIG = DATA_DIR / "open_flood_config.json"
ARCHIVO_TABLERO = DATA_DIR / "tablero.png"

COLORES = ["rojo", "azul", "verde", "amarillo", "naranja", "morado"]


def guardar_configuracion(datos):
    DATA_DIR.mkdir(exist_ok=True)
    with open(ARCHIVO_CONFIG, "w", encoding="utf-8") as archivo:
        json.dump(datos, archivo, indent=4)


def calibrar_tablero():
    input("Coloca el cursor en la esquina superior izquierda del tablero y presiona ENTER...")
    x1, y1 = pyautogui.position()

    input("Coloca el cursor en la esquina inferior derecha del tablero y presiona ENTER...")
    x2, y2 = pyautogui.position()

    return {
        "x": min(x1, x2),
        "y": min(y1, y2),
        "ancho": abs(x2 - x1),
        "alto": abs(y2 - y1)
    }


def capturar_tablero(region):
    time.sleep(1)
    imagen = pyautogui.screenshot(
        region=(region["x"], region["y"], region["ancho"], region["alto"])
    )
    imagen.save(ARCHIVO_TABLERO)


def calibrar_botones(lista_colores):
    coordenadas = {}
    for color in lista_colores:
        input(f"Coloca el cursor en el botón '{color}' y presiona ENTER...")
        x, y = pyautogui.position()
        coordenadas[color] = {"x": x, "y": y}
    return coordenadas


def calibrar_popup():
    input("Cuando aparezca el popup blanco, coloca el cursor en una zona blanca y presiona ENTER..")
    x, y = pyautogui.position()
    return {"x": x, "y": y}


def main():
    datos = {}
    datos["tablero"] = calibrar_tablero()
    capturar_tablero(datos["tablero"])
    print("Tablero inicial capturado correctamente.")
    datos["botones"] = calibrar_botones(COLORES)
    datos["popup"] = calibrar_popup()
    guardar_configuracion(datos)
    print("Calibración completada.")

main()
