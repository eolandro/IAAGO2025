from ruamel.yaml import YAML
from pathlib import Path

def generar_configuracion_base():
    yaml = YAML()
    while True:
         num_animales = int(input("Ingrese el número de animales (mínimo 10): "))
         if num_animales >= 10:
             break
         else:
             print("El número de animales debe ser mínimo 10.")
             
    while True:
        num_caracteristicas = int(input("Ingresa la cantidad de características: "))
        if num_caracteristicas > 0:
            break
        else:
            print("Cantidad invalida.")
            
    print(f"--------ANIMALES-------")
    animales = []
    for i in range(num_animales):
        nombre = input(f"Ingrese el nombre del animal #{i+1}: ").strip().capitalize()
        animales.append(nombre)
            
    print(f"\n-------CARACTERÍSTICAS-----")
    caracteristicas = []
    for i in range(num_caracteristicas):
        pregunta = input(f"Ingrese la característica {i+1}: ").strip()
        caracteristicas.append(pregunta)
    animalesy = {
        'animales': animales,
        'caracteristicas': caracteristicas
    }
    res = Path('animales.yaml')
    try:
        with open(res, 'w', encoding='utf-8') as archivo:
            yaml.dump(animalesy, archivo)
        print(f"Archivo creado")
    except Exception as e:
        print(f"Error: {e}")

generar_configuracion_base()
