import yaml

with open("mensajes1.yaml", 'r', encoding='utf-8') as file:
    mensajes = yaml.safe_load(file)

print("\nIndica si cada mensaje es spam o no, marcando con (s/n):\n")

resultado = {}

for i, mensaje in enumerate(mensajes, 1):
    while True:
        respuesta = input(f"Mensaje {i}: \n{mensaje}\nR = ").lower()
        if respuesta.startswith('s') or respuesta.startswith('n'):
            resultado[f"m{i}"] = {
                "texto": mensaje,
                "spam": respuesta.startswith('s')
            }
            print()
            break
        else:
            print("Para cada mensaje, ingresa 's' si es spam, 'n' si no lo es\n")

with open("respuestas1.yaml", 'w', encoding='utf-8') as file:
    yaml.dump(resultado, file, default_flow_style=False, allow_unicode=True)


total_spam = sum(1 for info in resultado.values() if info["spam"])
total_no_spam = len(resultado) - total_spam


print("========== RESUMEN DEL ENTRENADOR ==========")
print("Se procesaron los mensajes del archivo 'mensajes1.yaml'.\n")
print(f"Mensajes totales clasificados: {len(resultado)}")
print(f"SPAM: {total_spam}")
print(f"NO SPAM: {total_no_spam}")
print("\nClasificaciones guardadas en 'respuestas1.yaml'\n")
