from ruamel.yaml import YAML
from pathlib import Path

def registrar_datos():
    print("=== INICIALIZADOR - DATOS BÁSICOS ===")
    
    # Solo nombres de animales
    animales = []
    num_animales = int(input("¿Cuántos animales?: "))
    
    for i in range(num_animales):
        nombre = input(f"Animal {i+1}: ").strip()
        animales.append(nombre)
    
    caracteristicas = []
    num_carac = int(input("¿Cuántas características?: "))
    
    for i in range(num_carac):
        nombre = input(f"Característica {i+1}: ").strip().replace(' ', '_')
        if nombre and nombre not in caracteristicas:
            caracteristicas.append(nombre)
 
    yaml = YAML()
    yaml.indent(mapping=2, sequence=4, offset=2)
    
    datos_basicos = {
        'animales': animales,
        'caracteristicas': caracteristicas
    }
    
    archivo = Path('red_semantica.yaml')
    with archivo.open('w', encoding='utf-8') as f:
        yaml.dump(datos_basicos, f)
    
    print(f"\n✅ Datos básicos guardados")
    print("🎯 Ahora ejecuta: python entrenador.py")

if __name__ == '__main__':
    registrar_datos()
