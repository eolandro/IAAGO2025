from ruamel.yaml import YAML
import re
import spacy

yaml = YAML()
try:
    nlp = spacy.load("es_core_news_sm")
except IOError:
    print("Error: Modelo 'es_core_news_sm' no encontrado.")
    exit()

try:
    with open("tabla_probabilidades.yaml", 'r', encoding='utf-8') as entrada:
        datos_prob = yaml.load(entrada)
except FileNotFoundError:
    print("No se encontró 'tabla_probabilidades.yaml'")
    print("Por favor, ejecute 'DeTokenizador.py' primero.")
    exit()

# 2. Cargar los 10 mensajes nuevos a clasificar
try:
    with open("mensajes_clasif.yaml", 'r', encoding='utf-8') as entrada:
        datos_nuevos = yaml.load(entrada)
except FileNotFoundError:
    print("No se encontró 'mensajes_clasif.yaml'")
    exit()

probabilidades = datos_prob['probabilidades']
mensajes_nuevos = datos_nuevos['mensajes']
mensajes_clasificados = []

if probabilidades:
    umbral = sum(probabilidades.values()) / len(probabilidades)
else:
    umbral = 0.5 
print(f"Umbral de probabilidad para SPAM: {umbral:.4f}")

for msj in mensajes_nuevos:
    texto_limpio = re.sub(r'[^\w\s]', '', msj).lower()
    doc = nlp(texto_limpio)
    tokens_utiles = [token.text for token in doc if token.pos_ in ("NOUN", "VERB", "ADJ")]

    probs_mensaje = []
    for token in tokens_utiles:
        if token in probabilidades:
            probs_mensaje.append(probabilidades[token])
    
    if probs_mensaje:
        promedio_mensaje = sum(probs_mensaje) / len(probs_mensaje)
    else:
        promedio_mensaje = 0 
        
    es_spam = promedio_mensaje >= umbral

    print(f'\nMensaje: "{msj}"')
    print(f'  Promedio: {promedio_mensaje:.4f} -> Clasificado como: {"SPAM" if es_spam else "NO SPAM"}')
    
    mensajes_clasificados.append({msj: es_spam})

datos_nuevos['mensajes'] = mensajes_clasificados
with open("mensajes_clasificados.yaml", 'w', encoding='utf-8') as salida:
    yaml.dump(datos_nuevos, salida)


print("  Mensajes nuevos clasificados  ")
