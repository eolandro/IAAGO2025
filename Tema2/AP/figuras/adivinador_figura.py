from ruamel.yaml import YAML
from pathlib import Path

def adivinar_figura_grafo():
    yaml = YAML()
    archivo_grafo = Path('figuras_grafo.yaml') 

    try:
        with open(archivo_grafo, 'r', encoding='utf-8') as file:
            datos_grafo = yaml.load(file)
    except Exception as e:
        print(f"Error al cargar el archivo YAML: {e}")
        return

    transiciones = {}
    for origen, respuesta, destino in datos_grafo.get('Transiciones', []):
        if origen not in transiciones:
            transiciones[origen] = {}
        if isinstance(respuesta, str) and respuesta.isdigit():
            respuesta = int(respuesta)
        transiciones[origen][respuesta] = destino

    estado_actual = 'P_RAIZ'
    figura_adivinada = None
    
    while figura_adivinada is None: 
        
        if estado_actual.startswith('F_'): 
            figura_adivinada = datos_grafo['Preguntas'][estado_actual]
            break
            
        pregunta_texto = datos_grafo['Preguntas'][estado_actual]
        
        while True:
            respuesta_str = input(f"\n{pregunta_texto} (SI/NO o número): ").strip().upper()
            
            if respuesta_str in ['SI', 'S', '1']:
                respuesta_clave = 'SI'
            elif respuesta_str in ['NO', 'N', '0']:
                respuesta_clave = 'NO'
            else:
                respuesta_clave = respuesta_str
            if respuesta_clave in transiciones.get(estado_actual, {}):
                estado_actual = transiciones[estado_actual][respuesta_clave]
                break
            else:
                print("Respuesta inválida")
    
    if figura_adivinada:
        print(f"Tu figura es: {figura_adivinada}")
    else:
        print("figura desconocida")


adivinar_figura_grafo()
