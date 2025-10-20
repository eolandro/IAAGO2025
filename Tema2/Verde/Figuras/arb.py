import json

"""Construye un mapa de adyacencia desde la lista de transiciones."""
def construir_mapa_adj(transiciones):
    mapa = {}
    for padre, arista, hijo in transiciones:
        mapa.setdefault(padre, []).append((arista, hijo))
    return mapa

#***************************************************************************
def normaliza_respuesta(s: str) -> str:
    t = (s or "").strip().lower()

    respuestas_map = {
        "s": "Si", "si": "Si", "sí": "Si",
        "n": "No", "no": "No"
    }
    return respuestas_map.get(t, t)

#***************************************************************************
def recorrido_interactivo(nodo_id, preguntas, mapa_adj):
    texto = preguntas.get(nodo_id, "(Respuesta)")
    hijos = mapa_adj.get(nodo_id, [])

    # PRIMER IF - Caso base: nodo hoja
    if not hijos:
        mensaje_final = f"Tu figura es: {texto}" 
        print(f"\n********************************\n{mensaje_final}\n********************************")
        return

    pregunta = f"\n{texto} => "
    respuesta = input(pregunta)
    respuesta_norm = normaliza_respuesta(respuesta)

    for valor_arista, hijo in hijos:
        if valor_arista.lower() == respuesta_norm.lower():
            return recorrido_interactivo(hijo, preguntas, mapa_adj)

    print("\nLo siento, esa respuesta no es válida. Por favor, intenta de nuevo.")
    return recorrido_interactivo(nodo_id, preguntas, mapa_adj)

#***************************************************************************
def main():
    print("********************************")
    print("      Adivinador de Figuras")
    print("********************************")
    print("\n¡Bienvenido! Responde a las preguntas para adivinar tu figura.")
    print("Respuestas posibles: 'Si', 'No', o un número cuando se pida.\n")

    try:
        with open("TRANSICIONES.json", encoding='utf-8') as entrada:
            datos = json.load(entrada)

        # Este if se mantiene como parte de la validación principal
        if "A" not in datos.get("Preguntas", {}):
            print("Error: No se encontró el nodo raíz 'A' en la sección 'Preguntas' del JSON.")
            return

        mapa_adj = construir_mapa_adj(datos["Transiciones"])
        recorrido_interactivo("A", datos["Preguntas"], mapa_adj)

    except FileNotFoundError:
        print("Error: No se encontró 'TRANSICIONES.json'. Verifica que el archivo esté en la misma carpeta.")
    except KeyError as e:
        print(f"Error: El archivo JSON no tiene la clave requerida: {e}.")
    except Exception as e:
        print(f"Ocurrió un error inesperado: {e}")

if __name__ == "__main__":
    main()
