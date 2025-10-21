from ruamel.yaml import YAML
from pathlib import Path

def entrenar_sistema():
    yaml = YAML()
    
    # Cargar datos básicos
    archivo_basicos = Path('red_semantica.yaml')
    if not archivo_basicos.exists():
        print("Ejecuta primero: python inicializador.py")
        return
    
    with archivo_basicos.open('r', encoding='utf-8') as f:
        datos_basicos = yaml.load(f)
    
    animales_nombres = datos_basicos['animales']
    caracteristicas = datos_basicos['caracteristicas']
    
    print("=== ENTRENADOR - RECOLECCIÓN DE DATOS ===")
    print("Responde 1=Sí / 0=No para cada característica:\n")
    
    # Preguntar SÍ/NO para cada animal
    animales_completos = []
    
    for nombre_animal in animales_nombres:
        print(f"\n{nombre_animal.upper()}")
        animal = {'nombre': nombre_animal}
        
        for carac in caracteristicas:
            while True:
                resp = input(f"¿{nombre_animal} tiene '{carac.replace('_', ' ')}'? (1=Sí/0=No): ")
                if resp in ['0', '1']:
                    animal[carac] = int(resp)
                    break
                else:
                    print("Por favor ingresa 1 para Sí o 0 para No")
        
        animales_completos.append(animal)
        print(f"{nombre_animal} Listo")
    
    print("\n=== CALCULANDO ORDEN ÓPTIMO ===")
    
    caracteristicas_ordenadas = []
    for carac in caracteristicas:
        si = sum(1 for a in animales_completos if a.get(carac, 0) == 1)
        total = len(animales_completos)
        utilidad = 1 - abs(si/total - 0.5)  # Teoría de información
        caracteristicas_ordenadas.append((carac, utilidad, si, total-si))
    
    caracteristicas_ordenadas.sort(key=lambda x: x[1], reverse=True)
    
    # Mostrar orden óptimo
    print("\nORDEN ÓPTIMO DE PREGUNTAS:")
    for i, (carac, util, si, no) in enumerate(caracteristicas_ordenadas, 1):
        print(f"{i}. {carac.replace('_', ' ')} ({si} Sí, {no} No) - Utilidad: {util:.3f}")
    
    # Guardar conocimiento completo
    datos_completos = {
        'animales': animales_completos,
        'caracteristicas_orden': [c[0] for c in caracteristicas_ordenadas],
        'total_animales': len(animales_completos),
        'total_caracteristicas': len(caracteristicas)
    }
    
    archivo_completo = Path('tablaprecios.yaml')
    with archivo_completo.open('w', encoding='utf-8') as f:
        yaml.dump(datos_completos, f)
    
    print(f"\nSistema completo guardado en 'tablaprecios.yaml'")
    print("Ahora ejecuta: python adivinar.py")

if __name__ == '__main__':
    entrenar_sistema()
