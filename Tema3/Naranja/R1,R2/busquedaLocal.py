from ruamel.yaml import YAML

G = None

def llenarG(): # Va a traer lo del grafo y los va a pasar con esa funcion para que se pueda hacer la busqueda
    yaml = YAML()
    with open('grafo.yaml', 'r') as archivo:
        grafo = yaml.load(archivo)
    return grafo

def pP(G,R,B): 
    # Buscando primero en profundidad
    if R == B: # verificar si es el nodo actual
        return True
    if R in G:
        for hijo in G[R]:
            encontrado = pP(G, hijo, B)
            if encontrado:
                return True
    return False

def pA(G,R,B):
    # Buscando primero en anchura
    cola = [R]
    while cola:
        nodo_actual = cola.pop(0)
        if nodo_actual == B:
            return True
        if nodo_actual in G:
            cola.extend(G[nodo_actual])
    return False

G = llenarG()

# print(pA(G, 'A', 'AACB'))  
# print(pP(G, 'A', 'ACB'))   

while True:
    print("El nombre de las funciones es:")
    print("llenarG()-> para llenar el grafo")
    print("pP(G,raiz,buscar)-> para busqueda en profundidad")
    print("pA(G,raiz,busqueda)-> para busqueda en anchura\n")

    #Read
    READ = input(">")
    if READ == "salir()":
        break
    EVAL = eval(READ)
    print(EVAL)


    