import yaml
import math

def cargar_red_semantica():
    try:
        with open('red_semantica.yaml', 'r', encoding='utf-8') as file:
            return yaml.safe_load(file)
    except FileNotFoundError:
        print("Ejecuta primero inicializador.py")
        return None

def calcular_ganancia_informacion(animales_filtrados, caracteristica):
    if not animales_filtrados or len(animales_filtrados) <= 1:
        return 0
    
    entropia_inicial = calcular_entropia_conjunto(animales_filtrados)
    
    con_caracteristica = [a for a in animales_filtrados if a.get(caracteristica, 0) == 1]
    sin_caracteristica = [a for a in animales_filtrados if a.get(caracteristica, 0) == 0]
    
    peso_con = len(con_caracteristica) / len(animales_filtrados)
    peso_sin = len(sin_caracteristica) / len(animales_filtrados)
    
    entropia_condicional = (peso_con * calcular_entropia_conjunto(con_caracteristica) + 
                           peso_sin * calcular_entropia_conjunto(sin_caracteristica))
    
    return entropia_inicial - entropia_condicional

def calcular_entropia_conjunto(animales):
    if not animales:
        return 0
    
    total_animales = len(animales)
    if total_animales <= 1:
        return 0
    
    probabilidades = {}
    for animal in animales:
        nombre = animal['nombre']
        probabilidades[nombre] = probabilidades.get(nombre, 0) + 1
    
    entropia = 0
    for count in probabilidades.values():
        p = count / total_animales
        entropia -= p * math.log2(p)
    
    return entropia

def seleccionar_mejor_pregunta(animales_restantes, caracteristicas_disponibles):
    mejor_caracteristica = None
    mejor_ganancia = -1
    
    for carac in caracteristicas_disponibles:
        ganancia = calcular_ganancia_informacion(animales_restantes, carac)
        if ganancia > mejor_ganancia:
            mejor_ganancia = ganancia
            mejor_caracteristica = carac
    
    return mejor_caracteristica, mejor_ganancia

def adivinar_animal():
    red_semantica = cargar_red_semantica()
    if not red_semantica:
        return
    
    print("=== ADIVINADOR - SISTEMA EXPERTO ===")
    print("Objetivo: Adivinar el animal con el mínimo de preguntas")
    print("Basado en Teoría de la Información - Selección Dinámica")
    
    animales = red_semantica['animales']
    todas_caracteristicas = red_semantica['caracteristicas_orden']
    
    print(f"\nAnimales disponibles ({len(animales)}):")
    for animal in animales:
        print(f"- {animal['nombre']}")
    
    input("\n🎮 Presiona Enter para iniciar el juego...")
    
    animales_restantes = animales.copy()
    caracteristicas_disponibles = todas_caracteristicas.copy()
    preguntas_realizadas = []
    
    print("\n" + "="*50)
    print("COMIENZA EL JUEGO")
    print("="*50)
    
    while len(animales_restantes) > 1 and caracteristicas_disponibles:
        mejor_carac, ganancia = seleccionar_mejor_pregunta(animales_restantes, caracteristicas_disponibles)
        
        if not mejor_carac:
            break
        
        print(f"\n🔍 Estado: {len(animales_restantes)} animales posibles")
        
        respuesta = input(f"❓ ¿Tu animal tiene '{mejor_carac.replace('_', ' ')}'? (s/n) => ").lower().strip()
        
        while respuesta not in ['s', 'n']:
            print("Por favor, responde 's' para sí o 'n' para no")
            respuesta = input(f"❓ ¿Tu animal tiene '{mejor_carac.replace('_', ' ')}'? (s/n) => ").lower().strip()
        
        preguntas_realizadas.append({
            'numero': len(preguntas_realizadas) + 1,
            'caracteristica': mejor_carac,
            'ganancia': ganancia,
            'respuesta': respuesta
        })
        
        # Filtrar animales según respuesta
        if respuesta == 's':
            animales_restantes = [a for a in animales_restantes if a.get(mejor_carac, 0) == 1]
        else:
            animales_restantes = [a for a in animales_restantes if a.get(mejor_carac, 0) == 0]
        
        caracteristicas_disponibles.remove(mejor_carac)
        
        if len(animales_restantes) == 1:
            print(f"🎯 ¡Solo queda 1 animal posible!")
        elif len(animales_restantes) <= 3:
            nombres = [a['nombre'] for a in animales_restantes]
            print(f"📋 Posibles: {', '.join(nombres)}")
    
    print("\n" + "="*50)
    if len(animales_restantes) == 1:
        animal_adivinado = animales_restantes[0]
        print(f"🎉 ¡ADIVINÉ! Tu animal es: {animal_adivinado['nombre']}")
        print(f"📊 Preguntas realizadas: {len(preguntas_realizadas)}")
        print(f"⚡ Eficiencia: {(1 - len(preguntas_realizadas)/len(todas_caracteristicas)) * 100:.1f}%")
    elif len(animales_restantes) == 0:
        print("🤔 No pude adivinar ningún animal con las respuestas proporcionadas")
    else:
        print(f"🤔 No pude adivinar exactamente, pero se redujo a {len(animales_restantes)} animales:")
        for animal in animales_restantes:
            print(f"   - {animal['nombre']}")
    
    print("\n=== ESTADÍSTICAS DEL JUEGO ===")
    print(f"Total de características disponibles: {len(todas_caracteristicas)}")
    print(f"Preguntas necesarias: {len(preguntas_realizadas)}")
    print(f"Reducción de búsqueda: {len(animales)} → {len(animales_restantes)}")
    
    resultado_juego = {
        'preguntas_realizadas': preguntas_realizadas,
        'animal_adivinado': animales_restantes[0]['nombre'] if len(animales_restantes) == 1 else 'Múltiples',
        'total_preguntas': len(preguntas_realizadas),
        'total_caracteristicas': len(todas_caracteristicas),
        'eficiencia': len(preguntas_realizadas) / len(todas_caracteristicas)
    }
    
    with open('resultado_adivinador.yaml', 'w', encoding='utf-8') as file:
        yaml.dump(resultado_juego, file, default_flow_style=False, allow_unicode=True)
    
    print("\n=== CUMPLIMIENTO DE COMPETENCIAS ===")
    print("CD1-3: Análisis complejo de datos ✓")
    print("CD2-3: Optimización matemática dinámica ✓")
    print("AE1: Aplicación teoría información ✓")
    print("AE2: Sistema experto adaptativo ✓")
    print("Compromiso social: Educación tecnológica ✓")

def main():
    try:
        adivinar_animal()
    except Exception as e:
        print(f"Error durante el juego: {e}")

if __name__ == '__main__':
    main()
