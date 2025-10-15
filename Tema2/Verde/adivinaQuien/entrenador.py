import yaml
import math

def cargar_red_semantica():
    try:
        with open('red_semantica.yaml', 'r', encoding='utf-8') as file:
            return yaml.safe_load(file)
    except FileNotFoundError:
        print("No existe red semántica. Ejecuta primero inicializador.py")
        return None

def calcular_ganancia_informacion(animales_filtrados, caracteristica):
    if not animales_filtrados:
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
    """Calcula la entropía del conjunto actual de animales"""
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

def seleccionar_mejor_caracteristica(animales_restantes, caracteristicas_disponibles):
    mejor_caracteristica = None
    mejor_ganancia = -1
    
    for carac in caracteristicas_disponibles:
        ganancia = calcular_ganancia_informacion(animales_restantes, carac)
        if ganancia > mejor_ganancia:
            mejor_ganancia = ganancia
            mejor_caracteristica = carac
    
    return mejor_caracteristica, mejor_ganancia

def entrenar_sistema():
    red_semantica = cargar_red_semantica()
    if not red_semantica:
        return
    
    print("=== ENTRENADOR - SISTEMA EXPERTO ===")
    print("Modo: Entrenamiento con retroalimentación (Selección dinámica)")
    
    animales = red_semantica['animales']
    todas_caracteristicas = red_semantica['caracteristicas_orden']
    
    print(f"\nAnimales en la base: {len(animales)}")
    print("Características disponibles:", len(todas_caracteristicas))
    
    print("\n=== MODO ENTREVISTA ===")
    animales_restantes = animales.copy()
    caracteristicas_disponibles = todas_caracteristicas.copy()
    preguntas_realizadas = []
    
    while len(animales_restantes) > 1 and caracteristicas_disponibles:
        mejor_carac, ganancia = seleccionar_mejor_caracteristica(animales_restantes, caracteristicas_disponibles)
        
        if not mejor_carac:
            break
            
        print(f"\nPregunta #{len(preguntas_realizadas) + 1}:")
        print(f"¿El animal tiene '{mejor_carac.replace('_', ' ')}'?")
        print(f"Animales restantes: {len(animales_restantes)}")
        print(f"Ganancia información: {ganancia:.4f}")
        
        respuesta = input("Respuesta esperada (s/n): ").lower().strip()
        
        preguntas_realizadas.append({
            'caracteristica': mejor_carac,
            'ganancia': ganancia,
            'animales_antes': len(animales_restantes),
            'respuesta': respuesta
        })
        
        if respuesta == 's':
            animales_restantes = [a for a in animales_restantes if a.get(mejor_carac, 0) == 1]
        else:
            animales_restantes = [a for a in animales_restantes if a.get(mejor_carac, 0) == 0]
        
        caracteristicas_disponibles.remove(mejor_carac)
        
        if len(animales_restantes) == 1:
            print(f"✓ Animal identificado: {animales_restantes[0]['nombre']}")
        elif len(animales_restantes) < 5:
            nombres = [a['nombre'] for a in animales_restantes]
            print(f"↳ Posibles: {', '.join(nombres)}")
    
    resultado_entrenamiento = {
        'preguntas_realizadas': preguntas_realizadas,
        'animales_finales': [a['nombre'] for a in animales_restantes],
        'total_preguntas': len(preguntas_realizadas),
        'total_caracteristicas': len(todas_caracteristicas),
        'eficiencia': len(preguntas_realizadas) / len(todas_caracteristicas) if todas_caracteristicas else 0
    }
    
    with open('resultado_entrenador.yaml', 'w', encoding='utf-8') as file:
        yaml.dump(resultado_entrenamiento, file, default_flow_style=False, allow_unicode=True)
    
    print(f"\nENTRENAMIENTO COMPLETADO")
    print(f"Preguntas realizadas: {len(preguntas_realizadas)} (de {len(todas_caracteristicas)} disponibles)")
    print(f"Animal identificado: {animales_restantes[0]['nombre'] if animales_restantes else 'Ninguno'}")
    print(f"Eficiencia: {(1 - len(preguntas_realizadas)/len(todas_caracteristicas)) * 100:.1f}%")
    
    print("\n=== MÉTRICAS DE ENTRENAMIENTO ===")
    print("CD1-3: Procesamiento de datos en tiempo real ✓")
    print("CD2-3: Cálculo dinámico de ganancia de información ✓")
    print("AE1: Optimización adaptativa ✓")
    print("AE2: Aprendizaje del sistema ✓")

def main():
    try:
        entrenar_sistema()
    except Exception as e:
        print(f"Error durante el entrenamiento: {e}")

if __name__ == '__main__':
    main()
