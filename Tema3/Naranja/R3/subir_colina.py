import random
import json

G = None  # Grafo global

def llenarG():
    global G
    with open("grafo.json", "r", encoding="utf-8") as f:
        G = json.load(f)
    return "Grafo cargado correctamente\n"


def sC(G, inicio, objetivo):
    if G is None:
        return "Primero ejecuta llenarG()"

    print("¿Qué estrategia deseas usar?")
    print("Escribe 'c' para camino más corto o 'l' para camino más largo.")
    eleccion = input(">> ").strip().lower()

    if eleccion == "c":
        estrategia = "corto"
    elif eleccion == "l":
        estrategia = "largo"
    else:
        return "Opción no válida. Usa 'c' o 'l'."

    actual = inicio
    visitados = [actual]
    memoria = [actual]
    secuencias_previas = []  # Guarda secuencias y su contador

    while actual != objetivo:
        vecinos = []
        for nodo in G[actual]:
            peso = G[actual][nodo]
            if nodo not in memoria:
                vecinos.append((nodo, peso))

        if len(vecinos) == 0:
            print("No hay caminos disponibles desde", actual)
            break

        # Encontrar el mejor valor
        mejor_valor = vecinos[0][1]
        for nodo, peso in vecinos:
            if estrategia == "corto" and peso < mejor_valor:
                mejor_valor = peso
            if estrategia == "largo" and peso > mejor_valor:
                mejor_valor = peso

        # Buscar los candidatos con ese valor
        candidatos = [nodo for nodo, peso in vecinos if peso == mejor_valor]

        # Si hay empate, volado
        if len(candidatos) > 1:
            print("Empate detectado, haciendo volado...")
            siguiente = random.choice(candidatos)
        else:
            siguiente = candidatos[0]

        print("Desde", actual, "→", siguiente)

        actual = siguiente
        visitados.append(actual)

        # Actualizar memoria
        memoria.append(actual)
        if len(memoria) > 2:
            memoria.pop(0)

        # Verificar repeticiones (máximo 3 veces)
        if len(visitados) >= 3:
            secuencia = [visitados[-3], visitados[-2], visitados[-1]]
            repetido = False

            for s in secuencias_previas:
                if s["secuencia"] == secuencia:
                    s["veces"] += 1
                    repetido = True
                    if s["veces"] >= 3:
                        print("\nSe repitió la misma secuencia 3 veces. Terminando búsqueda.")
                        print("\nResumen del recorrido:")
                        print(" → ".join(visitados))
                        return ""
                    break

            if not repetido:
                secuencias_previas.append({"secuencia": secuencia, "veces": 1})

        if actual == objetivo:
            break

    print("\nResumen del recorrido:")
    print(" → ".join(visitados))
    return ""


# REPL
while True:
    READ = input(">")
    if READ.strip() == "salir()":
        print("Saliendo del programa.")
        break
    try:
        EVAL = eval(READ)
        print(EVAL)
    except Exception as e:
        print("Error:", e)
