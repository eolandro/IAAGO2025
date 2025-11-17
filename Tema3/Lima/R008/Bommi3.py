from pathlib import Path
import json
import argparse

def mapa():
    parser = argparse.ArgumentParser()
    parser.add_argument("Archivo", help="Archivo: ", type=Path)
    args = parser.parse_args()

    if args.Archivo.exists():
        print("Grafo encontrado")
        with args.Archivo.open('r') as arch_json:
            datos = json.load(arch_json)
            Mapa = datos["mapa"]
            return Mapa
    else:
        print("Archivo no encontrado")

# Heurística
def heuristica(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])

def recorrido(Mapa):
    b_bomie = None
    b_bomba = None
    for fila in range(len(Mapa)):
        for columna in range(len(Mapa[0])):
            # Buscamos a boomi
            if Mapa[fila][columna] == "B":
                b_bomie = (fila, columna)
            # Buscamos la bomba
            elif Mapa[fila][columna] == 2:
                b_bomba = (fila, columna)
    # Practiicamente buscamos el inicio y el fin
    # devolvemos las posiciones
    return b_bomie, b_bomba

def adyacentes(Mapa, casilla):
    filas = len(Mapa)
    columnas = len(Mapa[0])
    encontrados = []

    direcciones = [(0,1), (0,-1), (1,0), (-1,0)]

    for mx, my in direcciones:
        c_filas = casilla[0] + mx
        c_columnas = casilla[1] + my

        if c_filas < 0:
            continue
        if c_filas >= filas:
            continue
        if c_columnas < 0:
            continue
        if c_columnas >= columnas:
            continue
        if Mapa[c_filas][c_columnas] == 1:
            continue

        encontrados.append((c_filas, c_columnas))
    return encontrados


def buscar(Mapa):
    #bomie y bomba.
    # b_bomie, b_bomba que son del recorrido
    inicio, fin = recorrido(Mapa)
    if not inicio or not fin:
        return False #Si nos peta es por que falta una psicion

    #caminos posibles
    cola = [(inicio, [inicio], 0)]
    visitados = []

    while cola:
        # se toma el primero de la cola
        actual, camino, valor = cola[0]
        #sACAMOS EL PRIMERO
        cola = cola[1:]

        if actual == fin:
            #print("BOOOOMBA ")
            #print(camino)
            mostrar(Mapa, camino)
            return True

        visitados.append(actual)
        #Calculamos las casillas libres
        vecinos = adyacentes(Mapa, actual)
        for v in vecinos:
            #solo vecinos
            if v not in visitados:
                # aplicamos heurística 
                h = heuristica(v, fin)
                #v es la nueva casilla, depues el nuevo caqmino y el nuevo valor
                #agregamos vecino ala  cola
                cola.append((v, camino + [v], valor + 1 + h))
                #nuevo = (v, camino + [v], valor + 1 + h)
                # ordenamos la cola por el valor mas cercano(valor menor)
                cola.sort(key=lambda x: x[2])

                """pos = 0
                while pos < len(cola) and cola[pos][2] < nuevo[2]:
                    pos += 1
                    cola.insert(pos, nuevo)"""

    print("SIn camino pa")
    return False


def mostrar(Mapa, camino):
    print("\nCamino encontrado:\n")
    nuevo = [fila[:] for fila in Mapa]
    for (x, y) in camino:
        if nuevo[x][y] == 0:
            nuevo[x][y] = "*"
    for fila in nuevo:
        print(" ".join(str(x) for x in fila))
    
    salida = {
        "valores":camino,
        "mapa": nuevo
    }

    with open("resultado.json", "w") as archivo:
        json.dump(salida, archivo, separators=(',', ':'))


def main():
    Mapa = mapa()
    if not Mapa:
        return
    for fila in Mapa:
        print(fila)

    buscar(Mapa)


if __name__ == "__main__":
    main()
