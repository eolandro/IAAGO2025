import time
import random

grafo = {
    'A': {'L': 20, 'B': 5, 'C': 5},
    'B': {'A': 5, 'F': 10},
    'C': {'A': 5, 'K': 15, 'D': 2, 'E': 4},
    'D': {'C': 2, 'E': 3},
    'E': {'C': 4, 'D': 3, 'F': 2},
    'F': {'E': 2, 'B': 10, 'I': 7, 'G': 3, 'L': 17},
    'G': {'F': 3, 'H': 3,'I':3},
    'H': {'G': 3, 'J': 10},
    'I': {'F': 7, 'G': 3},
    'J': {'H': 10,'K':1},
    'K': {'C': 15, 'J': 1},
    'L': {'A': 20, 'F': 17}
}

def greedy_with_memory(inicio, meta, max_reintentos=20):

    for intento in range(max_reintentos):
        print(f"\n\n REINTENTO {intento+1} \n")

        actual = inicio
        memoria = [None, None]  # memoria tabú
        ruta = [actual]

        for paso in range(200):

            print(f"NODO {actual}")
            print(f"Memoria prohibida: {memoria}")

            # Si se llegó al objetivo
            if actual == meta:
                return ruta

            vecinos = grafo[actual]
            print(f"Vecinos: {vecinos}")

            # Remover movimientos prohibidos
            opciones = {}
            for nodo, costo in vecinos.items():
                if nodo not in memoria:
                    opciones[nodo] = costo

            if not opciones:
                print("No hay opciones válidas, se reinicia.\n")
                break

            if meta in opciones:
                elegido = meta
                print(f"objetivo -> {elegido}")
            else:
                # Regla codiciosa: elegir el menor costo
                min_costo = None
                for c in opciones.values():
                    if min_costo is None or c < min_costo:
                        min_costo = c

                candidatos = []
                for n, c in opciones.items():
                    if c == min_costo:
                        candidatos.append(n)

                print(f"Costo mínimo permitido: {min_costo}")
                print(f"Candidatos: {candidatos}")

                elegido = random.choice(candidatos)

            print(f"Elegido: {elegido}\n")

            # Actualizar memoria (tabú FIFO)
            memoria = [memoria[-1], actual]

            actual = elegido
            ruta.append(actual)
            time.sleep(0.1)

    print("\nNO SE ENCONTRÓ RUTA\n")
    return None


inicio = input("Ingresa el nodo de inicio (A-L): ").upper()
meta = "K"

ruta = greedy_with_memory(inicio, meta)

if ruta:
    print("\nRUTA FINAL:")
    print(" -> ".join(ruta))
else:
    print("No fue posible encontrar ruta.")
