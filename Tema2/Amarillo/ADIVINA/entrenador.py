from ruamel.yaml import YAML

yaml = YAML()

Datos = False
data = {
    "encabezado": ["Animal", "Total"],
    "filas": []
}

with open("animales.yml") as entrada:
    cad = entrada.read()
    Datos = yaml.load(cad)

L_carac = []
print("\n-------------------------- E N T R E N A D O R --------------------------\n")
for carac in Datos['Caracteristicas']:
    # Insertar la característica en el encabezado antes de "Total"
    data["encabezado"].insert(-1, carac)

    print("Característica:\n")
    print(f"*****{carac}*****")
 
   
    for anima in Datos['Animales']:
        while True:
            resu = input(f'\nEl animal {anima} cumple la caracteristica(s/n) => ').lower()
            if resu in ['s', 'n']:
                break
            else:
                print("\nError: Debes ingresar 's' para sí o 'n' para no. Intenta de nuevo.\n")
        animal_encontrado = None
        
        if resu.lower() == 's':
            for fila in data["filas"]:
                if fila['nombre'] == anima:  # Comparar en minúsculas
                    animal_encontrado = fila
                    break

            if animal_encontrado:
                    # Agregar la nueva característica al animal existente
                    animal_encontrado['caracteristicas'][carac] = 1
            else:
                # Crear un nuevo animal con la característica
                nuevo_animal = {
                    "nombre": anima, 
                    "caracteristicas": {
                        carac: 1
                    }
                }

                data["filas"].append(nuevo_animal)

        else:
            for fila in data["filas"]:
                if fila['nombre'] == anima:  # Comparar en minúsculas
                    animal_encontrado = fila
                    break

            if animal_encontrado:
                    # Agregar la nueva característica al animal existente
                    animal_encontrado['caracteristicas'][carac] = 0
            else:
                # Crear un nuevo animal con la característica
                nuevo_animal = {
                    "nombre": anima, 
                    "caracteristicas": {
                        carac: 0
                    }
                }

                data["filas"].append(nuevo_animal)

   
for fila in data["filas"]:
    # Calcular el total automáticamente a partir de las características
    total_str = ''.join(str(valor) for valor in fila["caracteristicas"].values())   
    # Actualizar el campo Total
    fila['Total'] = total_str

import json

with open("tabla_pesos.json","w") as salida:
       json.dump(data,salida,indent=2)
print("Archivo tabla_pesos.json creado")

