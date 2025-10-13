import yaml
from pathlib import Path

def adivinador():
    # Verificar que existan ambos archivos
    archivo_animales = Path('animales.yaml')
    archivo_tabla = Path('tabla.yaml')
    
    if not archivo_animales.exists() or not archivo_tabla.exists():
        print("Error: No se encuentran los archivos necesarios")
        print("Asegúrate de que existan 'animales.yaml' y 'tabla.yaml'")
        return

    # Cargar datos
    with open(archivo_animales, 'r') as file:
        datos_animales = yaml.safe_load(file)
    
    with open(archivo_tabla, 'r') as file:
        datos_tabla = yaml.safe_load(file)
    
    caracteristicas = datos_tabla['caracteristicas']
    tabla_animales = datos_tabla['tabla_animales']
    
    print("=== ADIVINADOR ===")
    print("Piensa en uno de los siguientes animales:")
    
    # Ordenar animales por suma binaria (mayor a menor)
    animales_ordenados = sorted(
        tabla_animales.items(), 
        key=lambda x: x[1]['suma_binaria'], 
        reverse=True
    )
    
    for i, (animal, datos) in enumerate(animales_ordenados, 1):
        print(f"{i}. {animal}")
    
    print("\nResponde las siguientes preguntas con 'si' o 'no':")
    
    # Inicializar lista de animales candidatos
    candidatos = list(tabla_animales.keys())
    
    # Función para encontrar la mejor pregunta
    def encontrar_mejor_pregunta(candidatos, caracteristicas, tabla_animales):
        mejor_pregunta = None
        mejor_division = len(candidatos)  # Empezamos con la peor división posible
        
        for idx, caracteristica in enumerate(caracteristicas):
            # Contar cuántos candidatos tienen 1 y cuántos 0 para esta característica
            count_si = 0
            count_no = 0
            
            for animal in candidatos:
                if tabla_animales[animal]['respuestas'][idx] == 1:
                    count_si += 1
                else:
                    count_no += 1
            
            # La mejor pregunta es la que divide más equilibradamente los candidatos
            division_actual = abs(count_si - count_no)
            if division_actual < mejor_division and (count_si > 0 and count_no > 0):
                mejor_division = division_actual
                mejor_pregunta = (idx, caracteristica)
        
        return mejor_pregunta
    
    # Hacer preguntas hasta que quede un solo candidato
    while len(candidatos) > 1:
        mejor_pregunta = encontrar_mejor_pregunta(candidatos, caracteristicas, tabla_animales)
        
        # Si no hay preguntas útiles y quedan 2 candidatos, preguntar directamente
        if mejor_pregunta is None and len(candidatos) == 2:
            animal_pregunta = candidatos[0]
            while True:
                respuesta = input(f"\n¿Tu animal es un {animal_pregunta}? (si/no): ").strip().lower()
                if respuesta in ['si', 'sí', 's', '1']:
                    candidatos = [animal_pregunta]
                    break
                elif respuesta in ['no', 'n', '0']:
                    candidatos = [candidatos[1]]  # El otro animal
                    break
                else:
                    print("Por favor, responde 'si' o 'no'")
            break  # Salida del bucle principal
        
        # Si no hay preguntas útiles y hay más de 2 candidatos, usar la primera
        if mejor_pregunta is None:
            idx = 0
            caracteristica = caracteristicas[0]
        else:
            idx, caracteristica = mejor_pregunta
        
        # Hacer la pregunta
        while True:
            respuesta = input(f"\n{caracteristica} (si/no): ").strip().lower()
            if respuesta in ['si', 'sí', 's', '1']:
                valor_esperado = 1
                break
            elif respuesta in ['no', 'n', '0']:
                valor_esperado = 0
                break
            else:
                print("Por favor, responde 'si' o 'no'")
        
        # Filtrar candidatos basándose en la respuesta
        nuevos_candidatos = []
        for animal in candidatos:
            if tabla_animales[animal]['respuestas'][idx] == valor_esperado:
                nuevos_candidatos.append(animal)
        
        candidatos = nuevos_candidatos
        
        print(f"Animales restantes: {len(candidatos)}")
        if len(candidatos) <= 5:  # Mostrar solo si son pocos
            for animal in candidatos:
                print(f"  - {animal}")
    
    # Mostrar resultado
    if len(candidatos) == 1:
        print(f"\n¡Adiviné! Tu animal es: {candidatos[0]}")
    else:
        print("\nNo pude adivinar tu animal. Puede que haya un error en los datos.")

adivinador()