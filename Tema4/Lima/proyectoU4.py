import subprocess
import json
import os
from pathlib import Path
from typing import List
from PIL import Image
import numpy as np
import matplotlib.pyplot as plt

ADB = r"C:\platform-tools\adb.exe"
ARCHIVO_CALIBRACION = "calibracion.json"
MOVIMIENTOS = 31

PALETA = {
    0: {'rgb': (232, 56, 56), 'coord': None},     # rojo
    1: {'rgb': (120, 136, 248), 'coord': None},   # azul
    2: {'rgb': (56, 152, 56), 'coord': None},    # verde
    3: {'rgb': (248, 200, 40), 'coord': None},   # amarillo
    4: {'rgb': (248, 104, 72), 'coord': None},   # naranja
    5: {'rgb': (168, 56, 184), 'coord': None},   # morado
    'replay': {'rgb': None, 'coord': None},
}

COORDENADAS_TABLERO = (0, 0, 0, 0)

def adb_run(cmd: str):
    if not Path(ADB).exists():
        raise FileNotFoundError("adb no encontrado")
    return subprocess.run(f'{ADB} {cmd}', shell=True,
                          capture_output=True, text=True)

def adb_tap(x: int, y: int):
    adb_run(f"shell input tap {x} {y}")
    print(f" TAP EN ({x},{y})")

def tomar_screenshot(nombre="screen.png"):
    adb_run(f"exec-out screencap -p > {nombre}")
    return nombre

#calibrar
def guardar_calibracion():
    data = {
        "botones": {str(k): PALETA[k]["coord"] for k in PALETA},
        "tablero": list(COORDENADAS_TABLERO)
    }
    with open(ARCHIVO_CALIBRACION, "w") as f:
        json.dump(data, f, indent=2)

def cargar_calibracion():
    global COORDENADAS_TABLERO
    if not os.path.exists(ARCHIVO_CALIBRACION):
        return False
    with open(ARCHIVO_CALIBRACION, "r") as f:
        data = json.load(f)

    for k in PALETA:
        PALETA[k]["coord"] = (
            tuple(data["botones"].get(str(k)))
            if data["botones"].get(str(k)) else None
        )
    COORDENADAS_TABLERO = tuple(data["tablero"])
    print("Calibración cargada")
    return True

def mostrar_clicks(img_path, n, titulo):
    img = Image.open(img_path)
    plt.imshow(img)
    plt.title(titulo)
    plt.axis("off")
    pts = plt.ginput(n, timeout=0)
    plt.close()
    return [(int(x), int(y)) for x, y in pts]

def calibrar():
    global COORDENADAS_TABLERO
    p = tomar_screenshot()
    botones = mostrar_clicks(p, 6, "Clic en los 6 botones")
    for i, c in enumerate(botones):
        PALETA[i]["coord"] = c

    tablero = mostrar_clicks(p, 2, "Clic sup-izq y inf-der del tablero")
    COORDENADAS_TABLERO = (*tablero[0], *tablero[1])
    guardar_calibracion()

def color_promedio(img):
    arr = np.array(img)[..., :3]
    return tuple(arr.mean(axis=(0, 1)).astype(int))

def color_mas_parecido(rgb):
    mejor, dist = None, 1e18
    for k, v in PALETA.items():
        if isinstance(k, int):
            d = sum((rgb[i] - v['rgb'][i])**2 for i in range(3))
            if d < dist:
                mejor, dist = k, d
    return mejor

def obtener_matriz(img, n=18):
    w, h = img.size
    cw, ch = w // n, h // n
    return [
        [
            color_mas_parecido(
                color_promedio(
                    img.crop((c*cw, f*ch, (c+1)*cw, (f+1)*ch))
                )
            )
            for c in range(n)
        ]
        for f in range(n)
    ]

def normalizar_sin_repetidos(
    movs: List[int],
    longitud: int = MOVIMIENTOS
) -> List[int]:

    resultado = []
    colores_validos = [k for k in PALETA if isinstance(k, int)]

    def distinto(ultimo):
        for c in colores_validos:
            if c != ultimo:
                return c
        return colores_validos[0]

    for m in movs:
        if len(resultado) >= longitud:
            break
        if m not in colores_validos or (resultado and m == resultado[-1]):
            m = distinto(resultado[-1] if resultado else None)
        resultado.append(m)

    while len(resultado) < longitud:
        resultado.append(distinto(resultado[-1]))

    return resultado

try:
    from algoritmo import resolver_tablero
except Exception:
    def resolver_tablero(matriz):
        return [0] * MOVIMIENTOS

def main():
    resp = input("¿Quieres calibrar antes de empezar? (s/n): ").strip().lower()
        
    if resp == "s":
        calibrar()
    else:
        if not cargar_calibracion():
            print("No hay calibración guardada. Se debe calibrar.")
            calibrar()

    while True:
        path = tomar_screenshot()
        x1, y1, x2, y2 = COORDENADAS_TABLERO
        tablero = Image.open(path).crop((x1, y1, x2, y2))
        matriz = obtener_matriz(tablero)

        movs_raw = resolver_tablero(matriz)
        movs = normalizar_sin_repetidos(movs_raw)

        print("\nMOVIMIENTOS DEFINITIVOS (31, sin repetidos):")
        print(movs)

        for i, m in enumerate(movs, 1):
            x, y = PALETA[m]["coord"]
            print(f"{i}. Color {m}")
            adb_tap(x, y)

        if input("¿Volver a jugar? (s/n): ").lower() != "s":
            break
        if PALETA['replay']['coord'] is None:
            p = tomar_screenshot()
            PALETA['replay']['coord'] = mostrar_clicks(p, 1, "Botón replay")[0]
            guardar_calibracion()
        adb_tap(*PALETA['replay']['coord'])

if __name__ == "__main__":
    main()
