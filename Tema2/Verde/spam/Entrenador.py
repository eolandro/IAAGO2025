from ruamel.yaml import YAML

yaml = YAML()
datos = None


try:
    with open("mensajes_entren.yaml", 'r', encoding='utf-8') as entrada:
        datos = yaml.load(entrada)
except FileNotFoundError:
    print("No se encontró el archivo 'mensajes_entren.yaml'")
    exit()

print("--- ENTRENAMIENTO ---")
print("Clasifica los siguientes 10 mensajes:")

mensajes_etiquetados = []

for msj in datos['mensajes']:
    respuesta = ""
    while respuesta not in ['s', 'n']:
        respuesta = input(f'\nMensaje: "{msj}"\n¿Es Spam? (s/n) => ')
    
    es_spam = True if respuesta.lower() == 's' else False
    mensajes_etiquetados.append({msj: es_spam})

datos['mensajes'] = mensajes_etiquetados

with open("mensajes_etiquetados.yaml", 'w', encoding='utf-8') as salida:
    yaml.dump(datos, salida)


print("  Mensajes etiquetados guardados  ")
