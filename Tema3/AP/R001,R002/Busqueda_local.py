import collections
from ruamel.yaml import YAML
import os
import re

# ESTRUCTURA BASE
G = None

def llenarG():
    """Carga el grafo desde 'grafo.yaml' usando ruamel.yaml."""
    global G
    
    nombre_archivo = 'grafo.yaml'
    
    if not os.path.exists(nombre_archivo):
        return f"'{nombre_archivo}' no encontrado." 

    yaml_handler = YAML()
    
    with open(nombre_archivo, 'r') as file:
        data = yaml_handler.load(file)
        
        if 'ARBOL' in data:
            G = data['ARBOL']
            return "Grafo cargado" 
        else:
            return "Error: El archivo YAML invalido'."
        
def pP(G, R, B):
    if G is None:
        return "Use llenarG() primero"
        
    pila = [R]
    visitados = {R}
    padres = {R: None}
    
    while pila:
        nodo_actual = pila.pop()
        print(nodo_actual)
        if nodo_actual == B:
            ruta = []
            temp = nodo_actual
            while temp is not None:
                ruta.append(temp)
                temp = padres.get(temp)
            ruta.reverse()
            return f"Ruta DFS: {' -> '.join(ruta)}"

        for vecino in reversed(G.get(nodo_actual, [])):
            if vecino not in visitados:
                visitados.add(vecino)
                padres[vecino] = nodo_actual
                pila.append(vecino)
                
    return f"Fallo: El nodo {B} no es alcanzable desde {R} por DFS."

def pA(G, R, B):
    if G is None:
        return "Use llenarG() primero"

    cola = collections.deque([R])
    visitados = {R}
    padres = {R: None}
    
    while cola:
        nodo_actual = cola.popleft()
        print(nodo_actual)
        if nodo_actual == B:
            ruta = []
            temp = nodo_actual
            while temp is not None:
                ruta.append(temp)
                temp = padres.get(temp)
            ruta.reverse()
            return f"Ruta BFS: {' -> '.join(ruta)}"

        for vecino in G.get(nodo_actual, []):
            if vecino not in visitados:
                visitados.add(vecino)
                padres[vecino] = nodo_actual
                cola.append(vecino)
                
    return f"Fallo: El nodo {B} no es alcanzable desde {R} por BFS."

while True:
    READ = input("> ")
    if READ =="salir()":
        break
    EVAL = eval(READ)
    
    if EVAL is not None:
        print(EVAL)
