import cv2, numpy as np
import os, sys
import time
import pyautogui
import argparse
import glob
from config import B, C
from tablero import a as Analizar

def h(I):
    if I in B:
        Xb, Yb = B[I]
        pyautogui.moveTo(Xb, Yb, duration=0.5)
        time.sleep(0.2)
        pyautogui.click()
        print(f"Se precionó el botón: {C[I]['n']}")
        print(f"Presionar Ctrl + C para detener")
        time.sleep(0.5)
    else:
        print(f"No hay coordenadas para el color {I}")

def procesar_imagen(Img, Auto):
    R = Analizar(Img)
    
    if not R:
        print("Tablero no encontrado")
        return False
    
    G, Mc, Ga, Ta = R
    Ca = G[0][0]
    
    print(f"\n * Color Actual: {C[Ca]['n']}")
    print(f" * Color Recomendado: {C[Mc]['n']}")
    
    if Auto:
        print(f"\n Ejecutando automática...")
        print("=============================")
        
        for I in range(2, 0, -1):
            time.sleep(0.5)
        
        h(Mc)
    
    return True

def monitorear(Img, Auto):
    if Auto:
        print("  MODO AUTOMÁTICO ACTIVADO")
    else:
        print("  MODO VISUAL ACTIVADO")
    
    Procesadas = set()
    
    if os.path.exists(Img):
        procesar_imagen(Img, Auto)
        Procesadas.add(Img)
    
    try:
        while True:
            Actuales = set(glob.glob("img*.png"))
            
            for Img in sorted(Actuales - Procesadas):
                if procesar_imagen(Img, Auto):
                    Procesadas.add(Img)
                time.sleep(1)
            
            time.sleep(0.5)
            
    except KeyboardInterrupt:
        print("\nPrograma detenido")

def main():
    Parser = argparse.ArgumentParser(
        description='Analizador Open Flood', 
        formatter_class=argparse.RawTextHelpFormatter
    )
    
    Parser.add_argument('imagen', help='Imagen inicial (ej: img1.png)')
    
    Parser.add_argument('--auto', action='store_true', 
                       help='Ejecutar movimientos automáticamente')
    
    Parser.add_argument('--monitor', action='store_true', 
                       help='Monitorear imágenes continuamente')
    
    Args = Parser.parse_args()
    
    if not os.path.exists(Args.imagen):
        print(f"No se encontró: {Args.imagen}")
        sys.exit(1)
    
    print("=============================")
    print("          OPEN FLOOD         ")
    print("=============================")
    
    if Args.monitor:
        monitorear(Args.imagen, Args.auto)
    else:
        procesar_imagen(Args.imagen, Args.auto)

if __name__ == "__main__":
    main()
