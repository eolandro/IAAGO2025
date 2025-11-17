import json
from tabulate import tabulate
from unidecode import unidecode
import random

with open("tabla_pesos.json", encoding='utf-8') as f:
    datos = json.load(f)

def corregir(txt):
    if not txt:
        return ""
    txt = unidecode(txt)
    reemp = {'A+-': 'ñ', 'A!': 'á', 'A3n': 'ón', 'A@': 'é', 'A$': 'í'}
    for mal, bien in reemp.items():
        txt = txt.replace(mal, bien)
    return txt    
def mejocarac(anima, caracs):
    mej = None
    mejval = -1
    for idx in caracs:
        con = sum(1 for a in anima if a[idx] == 1)
        sin = len(anima) - con
        if con > 0 and sin > 0:
            bal = min(con, sin) / len(anima)
            if bal > mejval:
                mejval = bal
                mej = idx
    return mej

encabezado = [corregir(col) for col in datos["encabezado"]]
filascorr = []
for fila in datos["filas"]:
    fcorr = {
        "nom": corregir(fila["nombre"]),
        "caracs": {corregir(k): v for k, v in fila["caracteristicas"].items()},
        "Total": fila["Total"]
    }
    try:
        fcorr["val"] = int(fila["Total"], 2)
    except ValueError:
        fcorr["val"] = 0
    filascorr.append(fcorr)
filasord = sorted(filascorr, key=lambda x: x["val"], reverse=True)
tabla = []
for fila in filasord:
    ftabla = [fila["nom"]]
    for carac in encabezado[1:-1]:
        ftabla.append(fila["caracs"].get(carac, 0))
    ftabla.append(fila["Total"])
    tabla.append(ftabla)
print("\n--------------------------A D I V I N A D O R --------------------------\n")

print(tabulate(tabla, headers=encabezado, tablefmt="grid"))
print("\nEscoge a un animal de la tabla: \n")

matriz = [encabezado] + tabla
anima = matriz[1:]
caracsdisp = list(range(1, len(encabezado) - 1))
pregun = 0
maxpreg = 3
encon = False
while pregun < maxpreg and len(anima) > 1 and not encon:
    mejoridx = mejocarac(anima, caracsdisp)
    if mejoridx is None:
        mejoridx = random.choice(caracsdisp)
    preg = f"El animal que escogiste tiene {encabezado[mejoridx]}?"
    resp = input(f"{preg} (s/n) => ").lower().strip()
    if resp== "s":
        anima = [a for a in anima if a[mejoridx] == 1]
    else:
        anima = [a for a in anima if a[mejoridx] == 0]
    if mejoridx in caracsdisp:
        caracsdisp.remove(mejoridx)
    if len(anima) == 1:
        print(f"\n El animal que escogiste es: {anima[0][0]}\n")
        encon = True
        break
if not encon and len(anima) == 2:
    anim = anima.copy()
    random.shuffle(anim)
    animapreg = anim[0]
    animaalt = anim[1]
    if resp:
        print(f"\n El animal que escogiste es: {animapreg[0]}\n")
    else:
        print(f"\n El animal que escogiste es: {animaalt[0]}\n")
    encon = True
