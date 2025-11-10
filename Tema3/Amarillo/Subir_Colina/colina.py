import json
from collections import deque

class Nodo:
    def __init__(self, valor, padre=None):
        self.valor = valor
        self.padre = padre
        self.hijos = []
        self.costo_acumulado = 0  




Graph = []


def getjson():
    global Graph 
    with open('grafo.json') as indata:
        R = json.load(indata)
    Graph = []
    
    for nodo, conexiones in R['aristas'].items():
        for conexion in conexiones:
            Graph.append((nodo, conexion[0], conexion[1]))

def heuris(nod_act, nod_obj):
    if nod_act == nod_obj:
        return 100
    dis = abs(ord(nod_act) - ord(nod_obj))
    return max(0, 10 - dis)

def colina(G, root, Elem):
    nodos = set([aris[0] for aris in G] + [aris[1] for aris in G])
    if root not in nodos:
        print(f"Raíz '{root}' no encontrada en el grafo.")
        return
    nodo_act = Nodo(root)
    ruta = [root]
    t  = 0
    while nodo_act.valor != Elem:
        t += 1
        vecis = []
        for aris in G:
            if aris[0] == nodo_act.valor:
                veci = aris[1]
                cos = aris[2] if len(aris) > 2 else 1  
                objet = heuris(veci, Elem)
                vecis.append((veci, cos, objet))
        if not vecis:
            break
        vecis.sort(key=lambda x: x[2], reverse=True)
        mej_veci, cos, valor_obj = vecis[0]
        if mej_veci in ruta:
            for veci, cos, valor_obj in vecis[1:]:
                if veci not in ruta:
                    mej_veci, cos, valor_obj = veci, cos, valor_obj
                    break
            else:
                break
        nuevo = Nodo(mej_veci, nodo_act)
        nuevo.costo_acumulado = nodo_act.costo_acumulado  + cos
        nodo_act.hijos.append(nuevo)
        nodo_act = nuevo
        ruta.append(mej_veci)
        if t  > 20:
            break
    if nodo_act.valor == Elem:
        print(f"\n Nodo {Elem} Encontradoooo")
        print(f"recorrido: {ruta}")
        print(f"Costo total: {nodo_act.costo_acumulado }")
        return ruta
    else:
        print(f"\n Nodo {Elem} no Encontrado")
        print(f"Última recorrido visto: {ruta}")
        return False

def main():
    Ended = False
    while not Ended:
        cmd = input(":>")
        if cmd == "exit":
            Ended = True
            continue

        res = eval(cmd)
        if res is not None:
            print(res)

if __name__ == "__main__":
    main()