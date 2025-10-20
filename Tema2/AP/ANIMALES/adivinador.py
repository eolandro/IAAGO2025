from ruamel.yaml import YAML
from pathlib import Path

def calcular_diferencia_absoluta(candidatos_actuales, caracteristicas, tabla_animales, idx):
    count_si = 0
    count_no = 0
    
    for animal in candidatos_actuales:
        if tabla_animales[animal]['respuestas'][idx] == 1:
            count_si += 1
        else:
            count_no += 1
    diferencia_actual = abs(count_si - count_no)
    return diferencia_actual, count_si, count_no

def encontrar_mejor_pregunta(candidatos_actuales, caracteristicas, tabla_animales, hechas):
    mejor_pregunta_idx = None
    mejor_diferencia = len(candidatos_actuales)
    
    for idx, caracteristica in enumerate(caracteristicas):
        if idx in hechas:
            continue
        
        diferencia, count_si, count_no = calcular_diferencia_absoluta(
            candidatos_actuales, caracteristicas, tabla_animales, idx
        )
        if diferencia < mejor_diferencia and count_si > 0 and count_no > 0:
            mejor_diferencia = diferencia
            mejor_pregunta_idx = idx
        
        if mejor_diferencia == 0:
            break
    return mejor_pregunta_idx

def adivinador():
    yaml = YAML()
    archivo_tabla = Path('TablaPesos.yaml')
    
    with open(archivo_tabla, 'r', encoding='utf-8') as file:
        datos_tabla = yaml.load(file)
        
    caracteristicas = datos_tabla['caracteristicas']
    tabla_animales = datos_tabla['tabla_animales']
    
    animales_ordenados = sorted(
        tabla_animales.items(), 
        key=lambda item: item[1]['suma_binaria'], 
        reverse=True
    )
    
    print("\nAnimales:")
    for i, (animal, datos) in enumerate(animales_ordenados, 1):
        print(f"  {i}. {animal}")
        
    print("\nComencemos!!!")
    
    candidatos = list(tabla_animales.keys())
    preguntas_hechas_indices = set()
    
    while len(candidatos) > 1:
        idx_pregunta = encontrar_mejor_pregunta(candidatos, caracteristicas, tabla_animales, preguntas_hechas_indices)
        pregunta_texto = caracteristicas[idx_pregunta]
        
        while True:
            respuesta = input(f"\n{pregunta_texto} (si/no o 1/0): ").strip().lower()
            if respuesta in ['si', '1']:
                valor_esperado = 1
                break
            elif respuesta in ['no', '0']:
                valor_esperado = 0
                break
            else:
                print("respues no valida")
        
        nuevos_candidatos = [
            animal for animal in candidatos 
            if tabla_animales[animal]['respuestas'][idx_pregunta] == valor_esperado
        ]
        
        candidatos = nuevos_candidatos
        preguntas_hechas_indices.add(idx_pregunta)
        
        print(f"Quedan {len(candidatos)} candidatos.")
        
    if len(candidatos) == 1:
        print(f"Tu animal es: {candidatos[0]}")
        print(f"Total de preguntas hechas: {len(preguntas_hechas_indices)}")

adivinador()
