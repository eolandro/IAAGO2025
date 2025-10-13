import yaml
import re

palabras_eliminar = {
    'el','la','los','las','un','una','unos','unas','de','del','al','a','en','por','para','con','sin',
    'y','o','pero','mas','si','no','que','como','cuando','es','son','ser','fue','era','este','esta',
    'estos','estas','se','su','sus','mi','mis','tu','tus','nuestro','nuestra','yo','tú','usted',
    'nosotros','ellos','ellas','me','te','le','lo','la','les','los','las','suya','suyo','muy','ya',
    'aqui','alli','ahi','donde','porque','cual','quien','solo','tambien','entonces','pues','entre',
    'sobre','hasta','desde','todo','toda','cada','hacia','antes','despues'
}

with open("mensajes2.yaml", "r", encoding="utf-8") as f:
    mensajes_nuevos = yaml.safe_load(f)

with open("tabla_probabilidad.yaml", "r", encoding="utf-8") as f:
    tabla = yaml.safe_load(f)["probabilidades"]


# Clasificacion por promedio (Consenso)
def clasificar_mensaje(texto):
    palabras = re.findall(r"\b[a-záéíóúñ]+\b", texto.lower())
    palabras_filtradas = [p for p in palabras if p not in palabras_eliminar and len(p) > 2]

    if not palabras_filtradas:
        return 0.0, "datos_insuficientes"

    probabilidades = []
    for p in palabras_filtradas:
        if p in tabla:
            probabilidades.append(tabla[p]["P_spam"])

    if not probabilidades:
        return 0.0, "datos_insuficientes"  # si ninguna palabra está en la tabla

    promedio = sum(probabilidades) / len(probabilidades)
    etiqueta = "spam" if promedio >= 0.5 else "no_spam"
    return round(promedio, 3), etiqueta


# Procesar todos los mensajes
resultados = {}

for i, mensaje in enumerate(mensajes_nuevos, start=1):
    promedio, etiqueta = clasificar_mensaje(mensaje)
    resultados[f"m{i}"] = {
        "texto": mensaje,
        "promedio_P_spam": promedio,
        "clasificacion": etiqueta
    }

with open("respuestas2.yaml", "w", encoding="utf-8") as f:
    yaml.dump(resultados, f, allow_unicode=True)


total_spam = sum(1 for r in resultados.values() if r["clasificacion"] == "spam")
total_no_spam = sum(1 for r in resultados.values() if r["clasificacion"] == "no_spam")
total_insuf = sum(1 for r in resultados.values() if r["clasificacion"] == "datos_insuficientes")

print("========== RESULTADOS DEL CLASIFICADOR ==========\n")
print("Se procesaron los mensajes del archivo 'mensajes2.yaml'.")
print("Tomando en cuenta la probabilidad de las palabras del entrenamiento del archivo 'tabla_probabilidad.yaml'")
print("\nSe utilizó el método de consenso basado en el *promedio de probabilidades*\n")

print(f"Mensajes analizados: {len(resultados)}")
print(f"SPAM: {total_spam}")
print(f"NO SPAM: {total_no_spam}")
print(f"DATOS INSUFICIENTES: {total_insuf}\n")

print("Los resultados fueron guardados en 'respuestas2.yaml'\n")

