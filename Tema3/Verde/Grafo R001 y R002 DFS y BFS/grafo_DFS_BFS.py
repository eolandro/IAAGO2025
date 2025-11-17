import yaml
from collections import deque


def cargar_grafo_desde_yaml(nombre_archivo):
    with open(nombre_archivo, 'r') as archivo:
        grafo = yaml.safe_load(archivo)
    return grafo


# =====================================================================
#   FUNCIÓN PARA ENCONTRAR LOS HIJOS DENTRO DEL YAML 
# =====================================================================
def obtener_hijos(nodo, estructura):
    """
    Busca un nodo en toda la estructura YAML anidada y devuelve
    el diccionario de sus hijos.
    """
    if nodo in estructura:
        return estructura[nodo]

    for sub in estructura.values():
        if isinstance(sub, dict):
            resultado = obtener_hijos(nodo, sub)
            if resultado is not None:
                return resultado

    return None


# =====================================================================
#   DFS 
# =====================================================================
def dfs_recorrido(nodo, grafo, destino):
    print("Visitado:", nodo)

    if nodo == destino:
        print("\nDestino encontrado:", nodo)
        return True 

    hijos = grafo.get(nodo, {})
    for hijo in hijos:
        if dfs_recorrido(hijo, hijos, destino):
            return True  

    return False


# =====================================================================
#   BFS
# =====================================================================
def bfs_recorrido(inicio, estructura, destino):
    cola = deque([inicio])
    padres = {inicio: None}
    nivel = {inicio: 0}

    while cola:
        nodo = cola.popleft()
        print(f"Visitado: {nodo} (nivel {nivel[nodo]})")

        if nodo == destino:
            print("\nDestino encontrado:", nodo)
            # reconstruir camino
            camino = []
            while nodo is not None:
                camino.append(nodo)
                nodo = padres[nodo]
            camino.reverse()
            print("Camino (BFS):", " -> ".join(camino))
            return True

        hijos_dict = obtener_hijos(nodo, estructura)

        if hijos_dict is None:
            continue

        for hijo in hijos_dict.keys():
            if hijo not in padres:
                padres[hijo] = nodo
                nivel[hijo] = nivel[nodo] + 1
                cola.append(hijo)

    print("No se encontró el nodo", destino)
    return False


def main():
    grafo = cargar_grafo_desde_yaml("grafo.yaml")

    print("¿Qué tipo de recorrido deseas realizar?")
    print("1. Recorrido en profundidad (DFS)")
    print("2. Recorrido en anchura (BFS)")
    opcion = input("Elige 1 o 2: ")

    destino = input("¿A qué nodo quieres llegar desde A?: ")

    if opcion == "1":
        print("\nRecorrido en profundidad:")
        dfs_recorrido("A", grafo, destino)

    elif opcion == "2":
        print("\nRecorrido en anchura:")
        bfs_recorrido("A", grafo, destino)

    else:
        print("Opción no válida.")


if __name__ == "__main__":
    main()
