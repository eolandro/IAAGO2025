import json
from collections import deque

#Arbol

class Nodo:
    def __init__(self, valor):
        self.valor = valor
        self.hijos = []

    def agregar_hijo(self, nodo_hijo):
        self.hijos.append(nodo_hijo)

    def __repr__(self):
        return f"Nodo({self.valor})"

def crear_arbol(graph, nodo_raiz):
    raiz = Nodo(nodo_raiz)
    nodos = {nodo_raiz: raiz}

    for padre, hijo in graph:
        if padre not in nodos:
            nodos[padre] = Nodo(padre)
        if hijo not in nodos:
            nodos[hijo] = Nodo(hijo)
        nodos[padre].agregar_hijo(nodos[hijo])

    return nodos[nodo_raiz]



Graph = []

def getjson():
    R = []
    with open('grafo.json') as indata:
        R = json.load(indata)
    Graph.extend(R)

def mostrar_arbol(nodo, nivel=0):
    print('  ' * nivel + str(nodo))
    for hijo in nodo.hijos:
        mostrar_arbol(hijo, nivel + 1)


#busqueda por Profuncidad
def dfs(G, root, elem):
    nodos_grafo = set([arista[0] for arista in G] + [arista[1] for arista in G])
    if root not in nodos_grafo:
        print(f"Raíz '{root}' no encontrada en el grafo.")
        return
    raiz = crear_arbol(G, root)
    ruta_completa = []
    def buscar_nodo(nodo, elem):
        ruta_completa.append(nodo.valor)
        if nodo.valor == elem:
            print(f"Nodo {elem} encontrado")
            print(f"Ruta de nodos recorridos: {ruta_completa}")
            return True
        if not nodo.hijos:
            return False
        for hijo in nodo.hijos:
            if buscar_nodo(hijo, elem):
                return True
        return False
    if not buscar_nodo(raiz, elem):
        print(f"Nodo {elem} no encontrado")
    del raiz

#busqueda por anchura
def bfs(G,root,Elem):
    nodos_grafo = set([arista[0] for arista in G] + [arista[1] for arista in G])
    if root not in nodos_grafo:
        print(f"Raíz '{root}' no encontrada en el grafo.")
        return
    raiz = crear_arbol(G, root)
    cola = deque([raiz])
    ruta_completa = []
    while cola:
        nodo_actual = cola.popleft()
        ruta_completa.append(nodo_actual.valor)
        if nodo_actual.valor == Elem:
            print(f"Nodo {Elem} encontrado")
            print(f"Ruta de nodos recorridos: {ruta_completa}")
            return 
        for hijo in nodo_actual.hijos:
            cola.append(hijo)
    print(f"Nodo {Elem} no encontrado")
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