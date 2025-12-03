from pynput import mouse, keyboard
from ruamel.yaml import YAML
import os

T = 6  
B = {} 

print("="*60)
print("CALIBRACIÓN DE BOTONES \nCliquea y presiona ESPACIO \nCalibra 6 botones \nESC para cancelar")
print("="*60)

P = None  

Y = YAML()
Y.indent(mapping=2, sequence=4, offset=2)

def OC(X, Yc, Bt, Pr):  
    global P
    if Pr:
        P = (X, Yc)

def OP(K): 
    global I, P
    
    if K == keyboard.Key.esc:
        print("\nCancelado")
        return False
    
    if K == keyboard.Key.space:
        if P is not None:
            B[I] = P
            print(f"Botón {I}: {P}")
            I += 1
            
            if I > T:
                print("\n" + "="*60)
                print("Configuracion Completa")
                print("="*60)
                
                GC()  
                
                return False
            else:
                print(f"\nBotón {I}")
                P = None
        else:
            print("Cliquea primero")

def GC():  
    try:
        C = "calibraciones"
        if not os.path.exists(C):
            os.makedirs(C)
        
        R = os.path.join(C, "calibrarB.yaml")
        
        if os.path.exists(R):
            with open(R, "r") as F:
                D = Y.load(F) or {}
        else:
            D = {}
        
        BD = {} 
        for K, V in B.items():
            BD[f"boton_{K}"] = list(V)
        
        D['botones'] = BD
        
        with open(R, "w") as F:
            Y.dump(D, F)
        
        
    except Exception as E:
        print(f"Error: {E}")

with mouse.Listener(on_click=OC) as ML:
    with keyboard.Listener(on_press=OP) as KL:
        I = 1
        print(f"\nBotón {I} - Cliquea y ESPACIO")
        KL.join()
