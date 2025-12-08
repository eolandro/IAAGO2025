import random
from ruamel.yaml import YAML

yaml = YAML()
with open('mapa.yaml', 'r', encoding='utf-8') as file:
    c = yaml.load(file)

PDB = 0.9
PDV = 0.2
F = 10
C = 5
T = F * C
LB = 3

def detector(pbom):
    if pbom:
        return 1 if random.random() < PDB else 0
    else:
        return 1 if random.random() < PDV else 0

def bayes(pb, lectura):
    pnb = 1 - pb
    if lectura == 1:
        n = PDB * pb
        d = n + PDV * pnb
    else:
        n = (1 - PDB) * pb
        d = n + (1 - PDV) * pnb
    return n / d if d != 0 else 0

def VT(c, f, clm):
    lep = "ABCDE"[:clm]
    for fila in range(1, f + 1):
        for letra in lep:
            clave = f"{letra}{fila}"
            if clave not in c:
                raise ValueError(f"Casilla {clave} no encontrada en el YAML")

VT(c, F, C)

cr = T
dr = LB
bx = False
clm = "ABCDE"[:C]

for f in range(1, F + 1):
    if bx or dr <= 0:
        break
    if f % 2 == 0:
        lr = clm
    else:
        lr = reversed(clm)
    for letra in lr:
        if bx or dr <= 0:
            break
        clave = f"{letra}{f}"
        br = c[clave]
        l1 = detector(br)
        print("-"*60)
        print(f"DETECTOR: {l1}")
        if l1 == 1:
            prior = 1.0 / cr
            print(f"   Probabilidad inicial: {prior}")
            print(f"   No hay bomba: {1 - prior}")
            pbomba = bayes(prior, l1)
            print(f"   Probabilidad Actualizada: {pbomba}")
            print("-"*60)
            for r in range(2):
                lectura_extra = detector(br)
                print(f"Resultado de revision {r+2}: {lectura_extra}")
                if lectura_extra == 1:
                    print(f"   Probabilidad (ANTES) {r}: {pbomba}")
                    print(f"   No hay bomba {r}: {1 - pbomba}")
                    pbomba = bayes(pbomba, lectura_extra)
                    print(f"   Probabilidad Actualizada: {r}: {pbomba}")
                else:
                    vieja = pbomba
                    pbomba = bayes(pbomba, lectura_extra)
                    print(f"   Probabilidad (ANTES) {r}: {vieja}")
                    print(f"   No hay bomba {r}: {1 - vieja}")
                    print(f"   Probabilidad Actualizada: {pbomba}")
            if pbomba >= 0.5 and dr > 0:
                dr -= 1
                print(f"Bomba (DETECTADA): {clave}")
            else:
                print(f"{clave}: 0")
        else:
            print(f"{clave}: 0")
        if br == 1 and (l1 == 0 or pbomba < 0.5 or dr < 0):
            print(f"\nEl Boome a morido en {clave}")
            bx = True
        cr -= 1

print("-"*60)
print("Resultados:")
print("El Boome a morido" if bx else "Tablero Recorrido")
print(f"Desactivadores (UTILIZADOS): {LB - dr}")
print(f"Casillas (REVISADAAS): {T - cr}")
print(f"Casillas (RESTANTES): {cr}")
bomr = sum(1 for v in c.values() if v == 1)
print(f"Bombas del (TABLERO): {bomr}")
