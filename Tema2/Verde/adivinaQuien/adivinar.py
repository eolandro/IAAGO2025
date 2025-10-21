from ruamel.yaml import YAML
from pathlib import Path

def mejor_pregunta_simple(animales, preguntas_disponibles):
    mejor_pregunta = None
    mejor_diferencia = float('inf') 
    
    for pregunta in preguntas_disponibles:
        si_tienen = 0
        no_tienen = 0
        
        for animal in animales:
            if animal.get(pregunta, 0) == 1:
                si_tienen += 1
            else:
                no_tienen += 1
        
        diferencia = abs(si_tienen - no_tienen)
        total = len(animales)
        
        if diferencia < mejor_diferencia and total > 0:
            mejor_diferencia = diferencia
            mejor_pregunta = pregunta
    
    return mejor_pregunta

def adivinar_animal():
    yaml = YAML()
    
    archivo_principal = Path('red_semantica.yaml')
    archivo_tabla = Path('tablaprecios.yaml')
    
    if not archivo_principal.exists():
        print("Error: No se encuentra 'red_semantica.yaml'")
        print("Ejecuta primero: python inicializador.py")
        return
    
    if not archivo_tabla.exists():
        print("Error: No se encuentra 'tablaprecios.yaml'")
        print("Ejecuta primero: python entrenador.py")
        return
    
    with archivo_principal.open('r', encoding='utf-8') as f:
        datos_principal = yaml.load(f)
    
    with archivo_tabla.open('r', encoding='utf-8') as f:
        datos_tabla = yaml.load(f)
    
    # Obtener animales
    animales_nombres = datos_principal['animales']
    
    # Obtener preguntas ordenadas
    preguntas_orden = datos_tabla['caracteristicas_orden']
    
    # Obtener animales y características
    animales = datos_tabla['animales']
    
    print("=== ADIVINA EL ANIMAL ===")
    print(f"Base de datos: {len(animales)} animales, {len(preguntas_orden)} características")
    
    posibles = animales.copy()
    preguntas_hechas = 0
    preguntas_disponibles = preguntas_orden.copy()
    
    # Mostrar animales disponibles (opcional)
    print("\nAnimales en el sistema:")
    for animal in animales_nombres:
        print(f"   - {animal}")
    
    print("\nComenzando adivinanza inteligente...")
    
    while len(posibles) > 1 and preguntas_disponibles:
        pregunta = mejor_pregunta_simple(posibles, preguntas_disponibles)
        
        if pregunta is None:
            break
        #Preguntar
        resp = input(f"¿Tiene '{pregunta.replace('_', ' ')}'? (s/n): ").lower()
        
        #Validar
        while resp not in ['s', 'n']:
            print("Por favor responde 's' para Sí o 'n' para No")
            resp = input(f"¿Tiene '{pregunta.replace('_', ' ')}'? (s/n): ").lower()
        
        # Filtrar animales basado en la respuesta
        if resp == 's':
            nuevos_posibles = [a for a in posibles if a.get(pregunta, 0) == 1]
        else:
            nuevos_posibles = [a for a in posibles if a.get(pregunta, 0) == 0]
        
        # Verificar si la pregunta fue útil
        if len(nuevos_posibles) == len(posibles):
            print("Esa pregunta no eliminó ningún animal, saltando...")
        else:
            posibles = nuevos_posibles
            preguntas_hechas += 1
        
        # Remover la pregunta de las disponibles
        preguntas_disponibles.remove(pregunta)
        
        # Si solo queda 1, podemos terminar
        if len(posibles) == 1:
            break
    
    # RESULTADO FINAL
    print("\n" + "="*50)
    
    if len(posibles) == 1:
        animal_adivinado = posibles[0]['nombre']
        print(f"¡ADIVINÉ! Tu animal es: {animal_adivinado}")
                
    elif len(posibles) > 1:
        nombres = [a['nombre'] for a in posibles]
        print(f"No estoy 100% seguro, podría ser uno de estos:")
        for nombre in nombres:
            print(f"   - {nombre}")
    else:
        print("No encontré al animal que estabas pensando")
    
    print(f"\nResumen:")
    print(f"   Preguntas realizadas: {preguntas_hechas}")

if __name__ == '__main__':
    adivinar_animal()
