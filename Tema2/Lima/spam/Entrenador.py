import yaml
import re

# Archivo de entrada
archivo_txt = "10msjspam.txt"

# Leer contenido del archivo
with open(archivo_txt, "r", encoding="utf-8") as f:
    contenido = f.read()

# Ignorar líneas que sean solo SPAM o NO SPAM
contenido = re.sub(r'(?im)^\s*(SPAM|NO\s*SPAM)\s*$', '', contenido)

# Extraer los textos entre comillas (incluye saltos de línea)
mensajes = re.findall(r'"(.*?)"', contenido, re.DOTALL)

# Diccionario para guardar resultados
resultados = {}

print("=== Clasificador de mensajes (y = spam, n = no spam) ===")

# Preguntar por cada mensaje
for i, mensaje in enumerate(mensajes, start=1):
    print(f"\nMensaje {i}:\n{'-'*40}")
    print(mensaje.strip())
    print('-'*40)
    
    while True:
        respuesta = input("¿Es spam? (y/n): ").strip().lower()
        if respuesta in ("y", "n"):
            resultados[mensaje.strip()] = "spam" if respuesta == "y" else "no spam"
            break
        else:
            print("Entrada inválida. Escribe 'y' para spam o 'n' para no spam.")

# Guardar resultados en YAML
archivo_salida = "entrenador2.yaml"
with open(archivo_salida, "w", encoding="utf-8") as f:
    yaml.dump(resultados, f, allow_unicode=True, sort_keys=False)

print(f"\nClasificación guardada en '{archivo_salida}'")
