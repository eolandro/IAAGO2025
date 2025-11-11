from pathlib import Path
import json
import argparse
import random 

def leerGrafo():
    parser = argparse.ArgumentParser()
    parser.add_argument("Archivo", help="Archivo JSON del grafo", type=Path)
    args = parser.parse_args()

    if args.Archivo.exists():
        print("Grafo encontrado")
        with args.Archivo.open('r') as arch_json:
            datos = json.load(arch_json)
            grafo=datos["Grafo"]
            #grafo2=datos["Grafo2"]
            #print(grafo)
            print("#Camilo largo")
            print("Ejemplo de uso: colina(grafo,\"L\",\"F\")")
            return grafo #, grafo2
    else:
        print("Archivo no encontrado")

def colina(G,R,B):
    #Camilo largo(Valores altos)
    visitados=[]

    while True:
        visitados.append(R)
        if R==B:
            print(f"Visitado:{R}")
            return True
        #Vecinos
        vecinos= [ (vecino, valor ) for nodo,vecino, valor in G if R== nodo]
        if not vecinos:
            return None
        #print(vecinos)
        #print(vecinos[:3])
        #return True

        #QQuitamos los ultimos dos visitados
        nuevos_vecinos = []
        for v, val in vecinos:
            if v not in visitados[-2:]:
                nuevos_vecinos.append((v, val))
        vecinos = nuevos_vecinos
        print(vecinos)
        #Mejor vecino
        op_Vecino=[None,None]# Ete es para el [vecinno | valor]
        
        for vecino, valor in vecinos:
            if op_Vecino[0] is None:
                op_Vecino[0]=vecino
                op_Vecino[1]=valor
            elif valor > op_Vecino[1]:
                op_Vecino[0]=vecino
                op_Vecino[1]=valor
            elif valor == op_Vecino[1]:
                op_Vecino[0] = random.choice([op_Vecino[0], vecino])
        
        #print(f"Elejido:{op_Vecino[0]}, Vale:{op_Vecino[1]}")
        
        R=op_Vecino[0]

        if len(visitados) > 3:
            visitados = visitados[-3:]


def main():
    grafo = leerGrafo()
    if grafo is None:
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