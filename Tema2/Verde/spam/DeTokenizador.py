from ruamel.yaml import YAML
import re
import spacy

try:
    nlp = spacy.load("es_core_news_sm")
except IOError:
    print("Error: Modelo 'es_core_news_sm' no encontrado.")
    exit()

yaml = YAML()
datos = None

try:
    with open("mensajes_etiquetados.yaml", 'r', encoding='utf-8') as entrada:
        datos = yaml.load(entrada)
except FileNotFoundError:
    print("No se encontró el archivo 'mensajes_etiquetados.yaml'")
    print("Por favor, ejecute 'entrenador.py' primero.")
    exit()

mensajes_spam = []

for msj_dict in datos['mensajes']:
    mensaje, es_spam = list(msj_dict.items())[0]
    if es_spam:
        mensajes_spam.append(mensaje)

print(f"Se encontraron {len(mensajes_spam)} mensajes de SPAM para procesar.")

listas_de_tokens = []
for texto in mensajes_spam:
    texto_limpio = re.sub(r'[^\w\s]', '', texto).lower()
    
    doc = nlp(texto_limpio)
    
    tokens_utiles = [token.text for token in doc if token.pos_ in ("NOUN", "VERB", "ADJ")]
    listas_de_tokens.append(tokens_utiles)

palabras_probabilidad = {}
total_mensajes_spam = len(listas_de_tokens)

if total_mensajes_spam > 0:
    vocabulario_spam = set(palabra for lista in listas_de_tokens for palabra in lista)

    for palabra in vocabulario_spam:
        cuenta = sum(1 for lista in listas_de_tokens if palabra in lista)
        
        probabilidad = cuenta / total_mensajes_spam
        palabras_probabilidad[palabra] = round(probabilidad, 4)

proba = {"probabilidades": palabras_probabilidad}

with open("tabla_probabilidades.yaml", 'w', encoding='utf-8') as salida:
    yaml.dump(proba, salida)

print("  Tabla de probabilidades generada  ")
