import pyautogui
import os
from ruamel.yaml import YAML

Y = YAML()

def cargar_calibracion():
    try:
        if not os.path.exists("calibraciones/calibrarC.yaml"):
            print("Sin calibración")
            print("   Ejecuta 'calibrarC.py'")
            return None, None
        
        with open("calibraciones/calibrarC.yaml", "r") as F:
            D = Y.load(F)
        
        if 'area_captura' not in D:
            print("Formato incorrecto - falta 'area_captura'")
            return None, None
        
        AC = D['area_captura']
        area = {}
        area[1] = tuple(AC['sup_izq'])
        area[2] = tuple(AC['sup_der'])
        area[3] = tuple(AC['inf_izq'])
        area[4] = tuple(AC['inf_der'])
        
        pos_blanco = None
        if 'posicion_blanco' in D:
            pos_blanco = tuple(D['posicion_blanco'])
        
        return area, pos_blanco
        
    except Exception as E:
        print(f"Error: {E}")
        return None, None

def verificar_blanco(pos_blanco):
    if pos_blanco is None:
        return False
    
    try:
        x, y = pos_blanco
        pixel = pyautogui.pixel(x, y)
        r, g, b = pixel
        es_blanco = (r > 200 and g > 200 and b > 200)
        
        if es_blanco:
            print(f"BLANCO DETECTADO en ({x}, {y}): RGB{pixel}")
        
        return es_blanco
        
    except Exception as E:
        print(f"Error al verificar blanco: {E}")
        return False

def tomar_captura():
    area, pos_blanco = cargar_calibracion()
    
    if area is None:
        return None, False
    
    try:
        x1, y1 = area[1]  
        x2, y2 = area[2]  
        x3, y3 = area[3]  
        x4, y4 = area[4]  
        
        L = min(x1, x3)    
        T = min(y1, y2)    
        R = max(x2, x4)    
        Bt = max(y3, y4)   
        
        W = R - L  
        H = Bt - T 
        
        if W <= 0 or H <= 0:
            return None, False
            
        juego_terminado = verificar_blanco(pos_blanco)
        
        C = "capturas"  
        if not os.path.exists(C):
            os.makedirs(C)
        
        i = 1
        while True:
            N = f"img{i}.png"  
            R = os.path.join(C, N) 
            if not os.path.exists(R):
                break
            i += 1
        
        S = pyautogui.screenshot(region=(L, T, W, H))
        S.save(R)
        
        return R, juego_terminado
        
    except Exception as E:
        print(f"Error: {E}")
        return None, False

print("\n" + "="*40)
print("   CAPTURADOR MEJORADO")
print("="*40)

ruta_captura, terminado = tomar_captura()
if ruta_captura:
    if terminado:
        print("¡JUEGO TERMINADO!")
else:
    print("Error al tomar captura")
