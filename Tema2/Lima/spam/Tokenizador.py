import yaml
import re
from collections import Counter

# Archivo YAML con las clasificaciones
archivo_yaml = "entrenador2.yaml"

# Cargar los datos
with open(archivo_yaml, "r", encoding="utf-8") as f:
    data = yaml.safe_load(f)

# Lista de palabras vacías (stopwords)
stopwords = {
    "a", "ante", "bajo", "cabe", "con", "contra", "de", "desde", "en", "entre",
    "hacia", "hasta", "para", "por", "según", "sin", "so", "sobre", "tras",
    "el", "la", "los", "las", "un", "una", "unos", "unas", "y", "o", "u", "e",
    "que", "se", "su", "sus", "al", "del", "es", "ha", "han", "como", "más",
    "muy", "por", "pero", "si", "no", "lo", "le", "les", "ya", "te", "tu",
    "esto", "eso", "aquí", "allí", "ser", "estar", "son", "fue", "fueron", "para"
}

# Extraer solo los mensajes de spam
mensajes_spam = [msg for msg, tipo in data.items() if tipo == "spam"]

# Tokenizar y limpiar
def limpiar_y_tokenizar(texto):
    palabras = re.findall(r'\b[a-záéíóúñ]+\b', texto.lower())
    return [p for p in palabras if p not in stopwords]

# Tokenizar todos los mensajes de spam
tokens_spam = [limpiar_y_tokenizar(m) for m in mensajes_spam]

# Contar frecuencia total
todas_palabras = [p for lista in tokens_spam for p in lista]
frecuencias = Counter(todas_palabras)

# Calcular probabilidad condicional de aparición
num_mensajes = len(mensajes_spam)
probabilidades = {}

for palabra in frecuencias:
    aparece_en = sum(1 for lista in tokens_spam if palabra in lista)
    probabilidades[palabra] = {
        "frecuencia": frecuencias[palabra],
        "probabilidad": round(aparece_en / num_mensajes, 4)
    }

# Ordenar por probabilidad descendente y quedarnos con las 10 primeras
top_15 = dict(sorted(probabilidades.items(), key=lambda x: x[1]["probabilidad"], reverse=True)[:15])

# Guardar en YAML
archivo_salida = "tokenizador2.yaml"
with open(archivo_salida, "w", encoding="utf-8") as f:
    yaml.dump(top_15, f, allow_unicode=True, sort_keys=False)

print(f"\nArchivo '{archivo_salida}' generado con las 10 palabras con mayor probabilidad.\n")
