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

with open("respuestas1.yaml", "r", encoding="utf-8") as f:
    mensajes = yaml.safe_load(f)

# Diccionario con conteos de aparición por palabra
palabras = {}

for msg_id, info in mensajes.items():
    texto = info["texto"].lower()
    es_spam = info["spam"]

    # Tokenización básica
    tokens = re.findall(r"\b[a-záéíóúñ]+\b", texto)

    # Filtro de palabras relevantes
    tokens_filtrados = {t for t in tokens if t not in palabras_eliminar and len(t) > 2}

    # Contar palabras únicas por mensaje
    for palabra in tokens_filtrados:
        if palabra not in palabras:
            palabras[palabra] = {"spam": 0, "no_spam": 0}
        palabras[palabra]["spam" if es_spam else "no_spam"] += 1


# Calcular probabilidades condicionales con suavizado de Laplace
probabilidades = {}
for palabra, conteo in palabras.items():
    total = conteo["spam"] + conteo["no_spam"]
    p_spam = (conteo["spam"] + 1) / (total + 2)
    p_no_spam = (conteo["no_spam"] + 1) / (total + 2)

    probabilidades[palabra] = {
        "P_spam": round(p_spam, 3),
        "P_no_spam": round(p_no_spam, 3),
        "apariciones_spam": conteo["spam"],
        "apariciones_no_spam": conteo["no_spam"],
        "total_apariciones": total
    }

with open("tabla_probabilidad.yaml", "w", encoding="utf-8") as f:
    yaml.dump({"probabilidades": probabilidades}, f, allow_unicode=True, sort_keys=True)
    

print("\n========== RESUMEN DEL DETOKENIZADOR ==========")
print("Se procesaron los mensajes del archivo 'respuestas1.yaml'.")
print("Se aplicó el *suavizado de Laplace* para el cálculo de las probabilidades condicionales,")
print("evitando probabilidades extremas (0 o 1) y mejorando la estabilidad del modelo.")
print(f"\nTabla de probabilidades generada con {len(probabilidades)} palabras significativas.")
print("Los resultados fueron guardados en 'tabla_probabilidad.yaml'\n")

