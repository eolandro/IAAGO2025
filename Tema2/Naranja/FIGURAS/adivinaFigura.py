import json
# Cargar el arbol 
try:
    with open("figuras.json", "r", encoding="utf-8") as f:
        arbol = json.load(f)
except FileNotFoundError:
    print("Error: No se encontró el archivo figuras.json")
    exit()

preguntas = arbol["Preguntas"]
transiciones = {}
for origen, respuesta, salida in arbol["Transiciones"]:
    transiciones[(origen, respuesta)] = salida

print("¡Bienvenido al juego 'Adivina la Figura'!")
print("Piensa en una de las siguientes figuras y yo intentaré adivinarla:")
print("""
- Círculo, Elipse
- Triángulos: Equilátero, Isósceles, Rectángulo, Escaleno
- Cuadriláteros: Cuadrado, Rectángulo, Rombo, Trapecio rectángulo
- Pentágono, Hexágono, Decágono, Estrella
""")

while True:  
    apuntador = "A"  # A es la raíz

    while True:
        respuestas_posibles = []
        for (origen, respuesta) in transiciones:
            if origen == apuntador:
                respuestas_posibles.append(respuesta)

        if not respuestas_posibles:   # si no hay transiciones, ya es el resultado
            print("\nResultado:", preguntas[apuntador])
            break

        print(preguntas[apuntador])
        
        while True:
            resp = input("> ").strip().capitalize()
            if resp in respuestas_posibles:
                break  # respuesta válida
            print("\nElige una opción válida:", respuestas_posibles)

        apuntador = transiciones[(apuntador, resp)]

    op = input("\n¿Quieres volver a jugar? (Si/No): ").strip().lower()
    if op != "si":
        print("Adiós")
        break