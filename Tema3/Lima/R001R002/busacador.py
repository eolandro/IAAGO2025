from pathlib import Path
import json
import argparse
 
#pP(grafo1 , 'A', 'ACBA') -> True
#pA(grafo1 , 'A', 'AAAA')  -> True
#pA(grafo1 , 'AA','AAAA') -> True
#pA(grafo1 , 'AA','ACBA') -> False
#pA(grafo1 , 'A', 'ACCCBA')  -> False

def leerGrafo():
    parser = argparse.ArgumentParser()
    parser.add_argument("Archivo", help="Archivo JSON del grafo", type=Path)
    args = parser.parse_args()

    if args.Archivo.exists():
        print("Grafo encontrado")
        with args.Archivo.open('r') as arch_json:
            datos = json.load(arch_json)
            grafo1=datos["Grafo1"]
            print("Ejemplo de uso: pP(grafo1 , 'A', 'ACBA')")
            print("Ejemplo de uso: pA(grafo1 , 'A', 'AAAA')")
            #grafo2=datos["Grafo2"]
            return grafo1 #, grafo2
    else:
        print("Archivo no encontrado")
    #print("Grafo1--------")
    #print(grafo1)
    #print("Grafo2--------")
    #print(grafo2)

# pP (búsqueda en profundidad)
# Grafo
# Raiz=A
# Buscar= ACBA
# Compara R vs B, (Se detiene cuando lo encuentra)
# Obtener hijos
# Marca raiz al primer hijo
# Continua con el siguiente hijo superior
def pP(G, R, B):
    if R not in G:
        for clave in G:
            if pP(G[clave], R, B):
                return True
        return False
    #print(f"Visitando: {R}")
    if R == B:
        #print(f"Encontrado: {B}")
        return True

    # Obtener hijos.
    if R in G:
        hijos = G[R]
    else:
        return False

    # Recorrer hijos
    for hijo in hijos:
        if pP(hijos, hijo, B):
            return True
    return False

# pQ (búsqueda en anchura)
# Grafo
# Raiz=A
# Buscar= ACBA
# Compara R vs B, (Se detiene cuando lo encuentra)<---    
# Obtener hijos y se agrega a la cola                 |
# Mueva raiz al siguiente elemento de la cola --------     
def pA(G, R, B):
    if R not in G:
        for clave in G:
            if pA(G[clave], R, B):
                return True
        return False
    cola = [(R, G)] 
    #print(cola)

    while cola:
        nodo, subgrafo = cola[0]# Obtener el primer elemento de la cola(que marcamos como raiz)
        cola = cola[1:]
        #print(f"Visitando: {nodo}")

        if nodo == B:
            #print(f"Encontrado: {B}")
            return True
        
        # obtener hijos. 
        if nodo in subgrafo:
            hijos = subgrafo[nodo]
        else:
            return False

        for hijo in hijos:
            cola.append((hijo, hijos))

    return False

def main():
    grafo1 = leerGrafo()
    if grafo1 is None:
        return

    while True:
        Read = input("> ")
        if Read.strip() == "exit":
            break
        try:
            EVAL = eval(Read)
            print(EVAL)
        except Exception as e:
            print("Error:", e)


if __name__ == "__main__":
    main()


