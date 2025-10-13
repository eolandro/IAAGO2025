import yaml

def inicializador():
    animales = []
    caracteristicas = []

    print("=== INICIALIZADOR ===")
    print("Ingresa 10 animales:")
    for i in range(10):
        animal = input(f"{i+1}. Animal: ").strip()
        animales.append(animal)

    print("\nIngresa 10 características (preguntas binarias como '¿Tiene pelaje?'):")
    for i in range(10):
        car = input(f"{i+1}. Característica: ").strip()
        caracteristicas.append(car)

    data = {
        'animales': animales,
        'caracteristicas': caracteristicas
    }

    with open('animales.yaml', 'w') as file:
        yaml.dump(data, file, default_flow_style=False, allow_unicode=True) 
        
#El default_flow_stile es para que se guarde de manera mas legible y el unicode permite acentos y ñ	
	
    print("\nArchivo 'animales.yaml' generado exitosamente")

inicializador()