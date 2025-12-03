import cv2, numpy as np
import os, sys
import time
import pyautogui
import argparse
import glob
from config import B, C
from tablero import a as A

def TC():  
    try:
        from ruamel.yaml import YAML
        Y = YAML()
        
        if not os.path.exists("calibraciones/calibrarC.yaml"):
            print("Ejecuta calibrarC.py")
            return None, False
        
        with open("calibraciones/calibrarC.yaml", "r") as F:
            D = Y.load(F)
        
        if 'area_captura' not in D:
            return None, False
        
        AC = D['area_captura']
        BA = {}
        BA[1] = tuple(AC['sup_izq'])
        BA[2] = tuple(AC['sup_der'])
        BA[3] = tuple(AC['inf_izq'])
        BA[4] = tuple(AC['inf_der'])
        
        x1, y1 = BA[1]
        x2, y2 = BA[2]
        x3, y3 = BA[3]
        x4, y4 = BA[4]
        
        L = min(x1, x3)
        T = min(y1, y2)
        R = max(x2, x4)
        Bt = max(y3, y4)
        
        W = R - L
        H = Bt - T
        
        if W <= 0 or H <= 0:
            return None, False
        
        CC = "capturas"
        if not os.path.exists(CC):
            os.makedirs(CC)
        
        i = 1
        while True:
            N = f"img{i}.png"
            R = os.path.join(CC, N)
            if not os.path.exists(R):
                break
            i += 1
        
        juego_terminado = False
        if 'posicion_blanco' in D:
            xb, yb = tuple(D['posicion_blanco'])
            pixel = pyautogui.pixel(xb, yb)
            r, g, b = pixel
            
            if r > 200 and g > 200 and b > 200:
                juego_terminado = True
        
        time.sleep(0.3)
        S = pyautogui.screenshot(region=(L, T, W, H))
        S.save(R)
        
        return R, juego_terminado
        
    except Exception as e:
        print(f"Error en captura: {e}")
        return None, False

def H(I):  
    if I in B:
        Xb, Yb = B[I]
        pyautogui.moveTo(Xb, Yb, duration=0.3)
        time.sleep(0.1)
        pyautogui.click()
        time.sleep(0.3)

def MJ(Auto, Lim=31):
    try:
        M = 0 
        
        while M < Lim:
            print(f"Movimiento {M+1}/{Lim}")
            
            RI, terminado = TC()  
            
            if terminado:
                print(f"\n{'='*50}")
                print("¡JUEGO TERMINADO DETECTADO!")
                print(f"Se jugaron {M} movimientos")
                print(f"{'='*50}")
                time.sleep(3)
                break
            
            if not RI:
                print("Error al capturar")
                time.sleep(1)
                continue
            
            print("Analizando tablero...")
            R = A(RI)
            
            if not R:
                time.sleep(1)
                continue
            
            G, Mc, Ga, Ta = R
            Ca = G[0][0]
            
            print(f"Color Actual: {C[Ca]['n']}")
            print(f"Color Recomendado: {C[Mc]['n']}")
            print(f"{'='*50}")
            
            if Ta >= 324:
                print(f"\n{'='*50}")
                print("¡TABLERO COMPLETO!")
                print(f"{'='*50}")
                time.sleep(3)
                break
            
            if Auto and Mc:
                H(Mc)
                M += 1
            
            time.sleep(1.0)
            
            if M >= Lim:
                time.sleep(3)
                break
            
    except KeyboardInterrupt:
        print("\n\nJuego interrumpido")
    except Exception as e:
        print(f"\nError: {e}")

def main():
    parser = argparse.ArgumentParser(description='Open Flood - Auto Player')
    
    parser.add_argument('--auto', action='store_true', help='Modo automático')
    parser.add_argument('--juego', action='store_true', help='Iniciar juego')
    parser.add_argument('--limite', type=int, default=31, help='Límite de movimientos')
    
    args = parser.parse_args()
    
    print("="*50)
    print("OPEN FLOOD - AUTO PLAYER")
    print("="*50)
    
    if args.juego:
        MJ(args.auto, args.limite)
    else:
        print("Uso: python main.py --juego --auto")
        print("\nPrimero ejecuta: python calibrarC.py")

if __name__ == "__main__":
    main()
