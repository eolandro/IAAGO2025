from ruamel.yaml import YAML
import json

# Crear una instancia de YAML
yaml = YAML()
yaml.preserve_quotes = True  # Mantiene las comillas
yaml.width = 1000            # Evita saltos de línea automáticos

# Cargar el primer archivo de probabilidades
with open("tablaprob.yaml", 'r', encoding='utf-8') as entrada:
    Datos = yaml.load(entrada)

# Cargar el segundo archivo de mensajes
with open("msjclasif.json", 'r', encoding='utf-8') as entrada:
    dat  = json.load(entrada)

# Obtener el diccionario de probabilidades
probabilidades = Datos['probabilidades']
 
# Calcular el promedio de las probabilidades globales
promedio_global = sum(probabilidades.values()) / len(probabilidades)

# Establecer un umbral para considerar la diferencia como indicativa de spam
umbral_diferencia = 0.02  # Umbral de diferencia ajustado

# Ciclo para comparar los mensajes y sus probabilidades
for i, mensaje in enumerate(dat['mensajes']):
    palabras = mensaje.split()  # Dividir el mensaje en palabras
    probabilidades_mensaje = []  # Lista para guardar probabilidades de este mensaje

    for palabra in palabras:
        palabra_limpia = palabra.strip('¡!¿?.,')  # Limpiar caracteres especiales
        if palabra_limpia.lower() in probabilidades:  # Comparar en minúsculas
            probabilidad = probabilidades[palabra_limpia.lower()]
            probabilidades_mensaje.append(probabilidad)  # Guardar probabilidad en la lista

    # Calcular el promedio de probabilidades para este mensaje
    if probabilidades_mensaje:  # Verificar si hay probabilidades
        promedio_mensaje = sum(probabilidades_mensaje) / len(probabilidades_mensaje)
    else:
        promedio_mensaje = 0  # Si no hay probabilidades, establecer promedio a 0

    # Calcular la diferencia entre el promedio del mensaje y el promedio global
    diferencia = abs(promedio_mensaje - promedio_global)

    # Clasificar el mensaje como spam si su promedio es mayor que el promedio global
    # o si la diferencia es mayor o igual a 0.07
    if promedio_mensaje > promedio_global or diferencia <= umbral_diferencia:
        clasificacion = True  # Spam
    else:
        clasificacion = False  # No spam

    # Guardar la clasificación en el diccionario 'dat'
    dat['mensajes'][i] = {mensaje: clasificacion}


# Guardar el archivo actualizado
with open("msjetq2.yaml", 'w', encoding='utf-8') as salida:
    yaml.dump(dat, salida)

print("\n" + "=" * 30)
print("     Mensajes Clasificados     ")
print("=" * 30,"\n")

