import random
from ruamel.yaml import YAML

yaml = YAML()
with open('mapa.yaml', 'r') as file:
    c = yaml.load(file) 

F = 10 
C = 5  
T = F * C 
LB = 3 

def detector(pbom): 
    if pbom:
        return 1 if random.random() < PDB else 0 
    else:
        return 1 if random.random() < PDV else 0 

PDB = 0.9  
PDV = 0.2  

def bayes(pb, lectura): 
   
    pnb = 1 - pb    
    
    if lectura == 1:  
        n = PDB * pb 
        d = n + (PDV * pnb) 
    else:  
        n = (1 - PDB) * pb
        d = n + ((1 - PDV) * pnb)
    
    return n / d if d != 0 else 0 

def VT(c, f, clm): 
    lep = "ABCDE"[:clm] 
    
    for f in range(1, f + 1):
        for letra in lep:
            clave = f"{letra}{f}"
            if clave not in c:
                raise ValueError(f"Casilla {clave} no encontrada en el YAML")

VT(c, F, C)
cr = T
dr = LB 
bx = False 
clm = "ABCDE"[:C]  

print("* * * * * * * * * * BOOME BAYES * * * * * * * * * *\n")
print(f"Configuración: {F} filas × {C} columnas = {T} casillas")
print(f"Desactivadores disponibles: {LB}\n")

for f in range(1, F + 1):
    if bx or dr <= 0:
        break
        
    if f % 2 == 0:  
        lr = clm 
        print("-"*60)
        print(f"Fila {f}: A --> E")
    else:  
        lr = reversed(clm)
        print("-"*60)
        print(f"Fila {f}: E --> A")

    for letra in lr:
        if bx or dr <= 0:
            break
            
        clave = f"{letra}{f}"
        br = c[clave] 
        
        print(f"  {clave}: ", end="")
        
        lectura = detector(br) 
        
        if lectura == 1:
            print("Posible bomba detectada")
            
            pbomba = 1.0 / cr 
            print(f"      Probabilidad inicial: {pbomba : .2%}")
            
            for r in range(2): 
                nl = detector(br)  
                pbomba = bayes(pbomba, nl)
                estado = "Se detecto bomba" if nl == 1 else "No se detecto bomba"
                print(f"      Revisión {r + 1}: {estado}  Probabilidad = {pbomba:.2%}")
            
            if pbomba >= 0.5 and dr > 0:
                dr -= 1
                print(f"     Bomba desactivada  ubicacion:{clave}")
                print(f"     Desactivadores restantes: {dr}")
            else:
                print(f"      Boome continua .... (Probalididad = {pbomba:.2%})")
                if br == 1:
                    print(f"\nBoome exploto!  ubicacion: {clave}")
                    bx = True
        else:  
            print("Vacío")
            if br == 1:
                print(f"\nBoome exploto!  ubicacion: {clave}")
                bx = True
        
        cr -= 1
        if bx:
            break

print("-"*60)
print("Resultados:")
if bx:
    print("Boome a modido")
else:
    print("Recorrido completo")
print(f"Desactivadores utilizados: {LB - dr}")
print(f"Casillas revisadas: {T - cr}")
print(f"Casillas restantes: {cr}")

bomr = sum(1 for valor in c.values() if valor == 1)
print(f"Bombas en el tablero: {bomr}")
