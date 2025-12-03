from pynput import mouse, keyboard
from ruamel.yaml import YAML
import os

print("="*60)
print("           CALIBRACIÓN COMPLETA")
print("="*60)
print("1. Calibra las 4 esquinas de la pantalla")
print("2. Calibra la POSICIÓN del BLANCO (fin de juego)")
print("="*60)
print("Instrucciones:")
print("- Mueve el cursor a la posición")
print("- Presiona ESPACIO para guardar")
print("- ESC para cancelar")
print("="*60)

T = 5  
P = None 
I = 1  
B = {}  

Y = YAML()
Y.indent(mapping=2, sequence=4, offset=2)

def OC(X, Yc, Bt, Pr): 
    global P
    if Pr:
        P = (X, Yc)
        nombres = ["Sup Izq P", "Sup Der P", 
                   "Inf Izq P", "Inf Der P",
                   "Posición Blanco"]

def OP(K): 
    global I, P
    
    if K == keyboard.Key.esc:
        print("\nCancelado")
        return False
    
    if K == keyboard.Key.space:
        if P is not None:
            B[I] = P
            nombres = ["Sup Izq P", "Sup Der P", 
                      "Inf Izq P", "Inf Der P",
                      "Posición Blanco"]
            print(f" {I} ({nombres[I-1]}): {P}")
            I += 1
            
            if I > T:
                print("\n" + "="*60)
                print("CALIBRACIÓN COMPLETA")
                print("="*60)
                
                GC()  
                
                return False
            else:
                nombres = ["Sup Izq P", "Sup Der P", 
                          "Inf Izq P", "Inf Der P",
                          "Posición Blanco"]
                print(f"\nSiguiente: {nombres[I-1]}")
                P = None
        else:
            print("Cliquea primero en la posición")

def GC(): 
    try:
        C = "calibraciones"
        if not os.path.exists(C):
            os.makedirs(C)
        
        R = os.path.join(C, "calibrarC.yaml")
        
        if os.path.exists(R):
            with open(R, "r") as F:
                D = Y.load(F) or {}
        else:
            D = {}
        
        D['area_captura'] = {
            'sup_izq': list(B[1]),
            'sup_der': list(B[2]),
            'inf_izq': list(B[3]),
            'inf_der': list(B[4])
        }
        
        D['posicion_blanco'] = list(B[5])
        
        with open(R, "w") as F:
            Y.dump(D, F)
        
    except Exception as E:
        print(f"Error: {E}")

with mouse.Listener(on_click=OC) as ML:
    with keyboard.Listener(on_press=OP) as KL:
        nombres = ["Sup Izq P", "Sup Der P", 
                  "Inf Izq P", "Inf Der P",
                  "Posición Blanco"]
        print(f"\n{nombres[I-1]} + ESPACIO")
        KL.join()
