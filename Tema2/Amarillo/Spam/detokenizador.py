from ruamel.yaml import YAML
import re
import spacy
# Cargar el modelo en español
nlp = spacy.load("es_core_news_sm")

yaml = YAML()
Datos = False
with open("msjetq.yaml", 'r', encoding='utf-8') as entrada:
       cad = entrada.read()
       Datos = yaml.load(cad)
mesj = []

for msj in Datos['mensajes']:
    for msje, val in msj.items():
        if val:
            mesj.append(msje)

for i in range(len(mesj)): 

    texto_sin_simbolos = re.sub(r'[^\w\s]', '', mesj[i])
    texto = texto_sin_simbolos.lower()
    doc = nlp(texto)
    mesj[i] = [token.text for token in doc if token.pos_ in ("NOUN", "VERB", "ADJ")]

# Guardar las palabras y contar cuántas veces se repiten
palabras_contadas = {}  # Diccionario para almacenar las palabras ya contadas y sus frecuencias
total_lineas = len(mesj)  # Número total de listas en mesj

for lista_palabras in mesj:
    for palabra in lista_palabras:
        if palabra not in palabras_contadas:
            # Contar la cantidad de veces que la palabra aparece en todas las listas
            cuenta = sum([lista.count(palabra) for lista in mesj])
            # Dividir el valor de cuenta entre el número total de líneas
            promedio = cuenta / total_lineas
            palabras_contadas[palabra] = round(promedio, 4)

proba = {"probabilidades": palabras_contadas}

with open("tablaprob.yaml", 'w', encoding='utf-8') as salida:
    yaml.dump(proba, salida)

print("\n" + "=" * 30)
print("     Tabla generada     ")
print("=" * 30,"\n")
