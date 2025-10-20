import yaml
import re

# === Archivos de entrada/salida ===
archivo_probabilidades = "tokenizador2.yaml"
archivo_mensajes_txt = "10msjspam2.txt"
archivo_salida = "clasificador2.yaml"

# === Cargar probabilidades ===
with open(archivo_probabilidades, "r", encoding="utf-8") as f:
    probabilidades = yaml.safe_load(f)

# === Leer mensajes desde el archivo TXT ===
with open(archivo_mensajes_txt, "r", encoding="utf-8") as f:
    contenido = f.read()

# Eliminar líneas que sean solo "SPAM" o "NO SPAM"
contenido = re.sub(r'(?im)^\s*(SPAM|NO\s*SPAM)\s*$', '', contenido)

# Extraer los mensajes entre comillas (soporta saltos de línea)
mensajes = re.findall(r'"(.*?)"', contenido, re.DOTALL)

print(f"\nSe encontraron {len(mensajes)} mensajes en '{archivo_mensajes_txt}'.\n")

# === Lista de stopwords (palabras comunes irrelevantes) ===
stopwords = {
    "a", "ante", "bajo", "cabe", "con", "contra", "de", "desde", "en", "entre",
    "hacia", "hasta", "para", "por", "según", "sin", "so", "sobre", "tras",
    "el", "la", "los", "las", "un", "una", "unos", "unas", "y", "o", "u", "e",
    "que", "se", "su", "sus", "al", "del", "es", "ha", "han", "como", "más",
    "muy", "por", "pero", "si", "no", "lo", "le", "les", "ya", "te", "tu",
    "esto", "eso", "aquí", "allí", "ser", "estar", "son", "fue", "fueron", "para"
}

def limpiar_y_tokenizar(texto):
    palabras = re.findall(r'\b[a-záéíóúñ]+\b', texto.lower())
    return [p for p in palabras if p not in stopwords]

# === Evaluar mensajes ===
clasificaciones = {}

for msg in mensajes:
    tokens = limpiar_y_tokenizar(msg)
    
    # Buscar las palabras que estén en las probabilidades
    probs = [probabilidades[p]["probabilidad"] for p in tokens if p in probabilidades]
    
    if probs:
        promedio = sum(probs) / len(probs)
    else:
        promedio = 0.0
    
    es_spam = promedio > 0.5  # Umbral del 50%
    
    clasificaciones[msg] = {
        "promedio": round(promedio * 100, 2),
        "clasificacion": "spam" if es_spam else "no_spam"
    }

# === Guardar resultados en YAML ===
with open(archivo_salida, "w", encoding="utf-8") as f:
    yaml.dump(clasificaciones, f, allow_unicode=True, sort_keys=False)

print(f"Archivo '{archivo_salida}' generado con las clasificaciones.\n")
