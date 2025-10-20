from ruamel.yaml import YAML
from pathlib import Path

def calcular_suma_binaria(respuestas):
    suma = 0
    n_caracteristicas = len(respuestas)
    for i, respuesta in enumerate(respuestas):
        peso = 2 ** (n_caracteristicas - 1 - i)
        suma += respuesta * peso
    return suma

def entrenador():
    yaml = YAML()
    archivo_animales = Path('animales.yaml')
    archivo_salida = Path('TablaPesos.yaml')

    with open(archivo_animales, 'r', encoding='utf-8') as file:
        animales_inicializador = yaml.load(file)
        
    animales = animales_inicializador.get('animales', [])
    caracteristicas = animales_inicializador.get('caracteristicas', [])

    tabla_final = {
        'caracteristicas': caracteristicas,
        'tabla_animales': {}
    }

    for animal in animales:
        print(f"\n----- {animal} -----")
        respuestas_binarias = []
        
        for pregunta in enumerate(caracteristicas):
            while True:
                respuesta = input(f"{pregunta[1]} (si/no o 1/0): ").strip().lower()
                
                if respuesta in ['si', 's', '1']:
                    valor = 1
                    break
                elif respuesta in ['no', 'n', '0']:
                    valor = 0
                    break
                else:
                    print("no es una repuesta valida")
            respuestas_binarias.append(valor)
        suma_binaria = calcular_suma_binaria(respuestas_binarias)
        
        tabla_final['tabla_animales'][animal] = {
            'respuestas': respuestas_binarias,
            'suma_binaria': suma_binaria
        }
        
        print(f"Resultado de {animal}: Respuestas={respuestas_binarias}, Suma Binaria={suma_binaria}")

    try:
        with open(archivo_salida, 'w', encoding='utf-8') as file:
            yaml.dump(tabla_final, file)
        print(f"archivo creado")
    except Exception as e:
        print(f"Error: {e}")

entrenador()
