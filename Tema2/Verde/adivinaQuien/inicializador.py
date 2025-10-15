import yaml
import math

def registrar_caracteristicas_interactivo():
    print("\n=== REGISTRO DE CARACTERÍSTICAS ===")
    
    while True:
        try:
            num_caracteristicas = int(input("¿Cuántas características vas a registrar para los animales? "))
            if num_caracteristicas > 0:
                break
            else:
                print("Por favor ingresa un número mayor a 0")
        except ValueError:
            print("Por favor ingresa un número válido")
    
    caracteristicas = []
    
    print(f"\nVamos a registrar {num_caracteristicas} características:")
    
    for i in range(num_caracteristicas):
        while True:
            carac_nombre = input(f"\nNombre de la característica #{i+1} (ej: 'Pelaje', 'Colmillos', 'Alas'): ").strip()
            
            if not carac_nombre:
                print("El nombre no puede estar vacío")
                continue
                
            carac_normalizada = carac_nombre.replace(' ', '_')
            
            if carac_normalizada in caracteristicas:
                print("Esta característica ya fue registrada")
                continue
                
            caracteristicas.append(carac_normalizada)
            print(f"✓ Característica '{carac_nombre}' registrada")
            break
    
    print(f"\nCaracterísticas registradas: {', '.join([c.replace('_', ' ') for c in caracteristicas])}")
    return caracteristicas

def registrar_animales_interactivo(caracteristicas):
    print("\n=== REGISTRO DE ANIMALES ===")
    
    while True:
        try:
            num_animales = int(input("¿Cuántos animales vas a registrar? "))
            if num_animales > 0:
                break
            else:
                print("Por favor ingresa un número mayor a 0")
        except ValueError:
            print("Por favor ingresa un número válido")
    
    animales = []
    
    print(f"\nVamos a registrar {num_animales} animales:")
    print("Para cada característica, ingresa:")
    print("  - 1 si el animal SÍ tiene la característica")
    print("  - 0 si el animal NO tiene la característica")
    
    for i in range(num_animales):
        print(f"\n" + "="*40)
        print(f"ANIMAL #{i+1}")
        print("="*40)
        
        nombre = input("Nombre del animal: ").strip()
        while not nombre:
            print("El nombre no puede estar vacío")
            nombre = input("Nombre del animal: ").strip()
        
        animal = {'nombre': nombre}
        
        print(f"\nRegistrando características para {nombre}:")
        
        for carac in caracteristicas:
            carac_legible = carac.replace('_', ' ')
            while True:
                valor_str = input(f"¿{nombre} tiene '{carac_legible}'? (1=Sí, 0=No): ").strip()
                if valor_str in ['0', '1']:
                    valor = int(valor_str)
                    animal[carac] = valor
                    break
                else:
                    print("Por favor ingresa 1 para Sí o 0 para No")
        
        animales.append(animal)
        print(f"✅ {nombre} registrado correctamente")
    
    return animales

def calcular_entropia(animales, caracteristica):
    total_animales = len(animales)
    if total_animales == 0:
        return 0
    
    con_caracteristica = sum(1 for animal in animales if animal.get(caracteristica, 0) == 1)
    sin_caracteristica = total_animales - con_caracteristica
    
    p1 = con_caracteristica / total_animales
    p0 = sin_caracteristica / total_animales
    
    entropia = 0
    if p1 > 0:
        entropia -= p1 * math.log2(p1)
    if p0 > 0:
        entropia -= p0 * math.log2(p0)
    
    return entropia

def mostrar_resumen_animales(animales, caracteristicas):
    print("\n" + "="*70)
    print("RESUMEN DE ANIMALES REGISTRADOS")
    print("="*70)
    
    print("{:<15}".format("ANIMAL"), end="")
    for carac in caracteristicas:
        print("{:<12}".format(carac.replace('_', ' ')[:10]), end="")
    print()
    print("-" * (15 + 12 * len(caracteristicas)))
    
    for animal in animales:
        print("{:<15}".format(animal['nombre']), end="")
        for carac in caracteristicas:
            valor = animal.get(carac, 0)
            simbolo = "✅" if valor == 1 else "❌"
            print("{:<12}".format(simbolo), end="")
        print()

def mostrar_estadisticas(animales, caracteristicas):
    print("\n=== ESTADÍSTICAS DE CARACTERÍSTICAS ===")
    
    for carac in caracteristicas:
        total_si = sum(1 for animal in animales if animal.get(carac, 0) == 1)
        total_no = len(animales) - total_si
        porcentaje_si = (total_si / len(animales)) * 100
        
        print(f"{carac.replace('_', ' '):<20}: {total_si:>2} Sí ({porcentaje_si:5.1f}%) | {total_no:>2} No")

def crear_red_semantica_interactiva():
    print("=== INICIALIZADOR INTERACTIVO - RED SEMÁNTICA ===")
    print("Basado en Teoría de la Información\n")
    
    caracteristicas = registrar_caracteristicas_interactivo()
    animales = registrar_animales_interactivo(caracteristicas)
    
    if not animales:
        print("No se registraron animales. Saliendo...")
        return None
    
    print(f"\n🎉 REGISTRO COMPLETADO:")
    print(f"   - Animales registrados: {len(animales)}")
    print(f"   - Características usadas: {len(caracteristicas)}")
    
    mostrar_resumen_animales(animales, caracteristicas)
    mostrar_estadisticas(animales, caracteristicas)
    
    print(f"\n=== CÁLCULO DE ENTROPÍAS ===")
    entropias = {}
    for carac in caracteristicas:
        entropia = calcular_entropia(animales, carac)
        entropias[carac] = entropia
        print(f"Entropía de '{carac.replace('_', ' ')}': {entropia:.4f}")
    
    caracteristicas_ordenadas = sorted(entropias.items(), key=lambda x: x[1], reverse=True)
    
    print("\n=== ORDEN ÓPTIMO DE PREGUNTAS ===")
    print("(De mayor a menor ganancia de información)")
    for i, (carac, entropia) in enumerate(caracteristicas_ordenadas, 1):
        print(f"{i:>2}. {carac.replace('_', ' '):<20} (entropía: {entropia:.4f})")
    
    red_semantica = {
        'metadata': {
            'total_animales': len(animales),
            'total_caracteristicas': len(caracteristicas),
            'fuente': 'registro_interactivo'
        },
        'caracteristicas_orden': [carac for carac, _ in caracteristicas_ordenadas],
        'entropias': entropias,
        'animales': animales
    }
    
    with open('red_semantica.yaml', 'w', encoding='utf-8') as file:
        yaml.dump(red_semantica, file, default_flow_style=False, allow_unicode=True, indent=2)
    
    print(f"\n💾 Red semántica guardada en 'red_semantica.yaml'")
    
    return red_semantica

def main():
    try:
        red_semantica = crear_red_semantica_interactiva()
        
        if red_semantica:
            print("\n=== RESUMEN DE EJECUCIÓN ===")
            print(f"Animales registrados: {red_semantica['metadata']['total_animales']}")
            print(f"Características procesadas: {red_semantica['metadata']['total_caracteristicas']}")
            print(f"Orden óptimo calculado: {len(red_semantica['caracteristicas_orden'])} preguntas")
            
            print("\n=== COMPETENCIAS CUMPLIDAS ===")
            print("CD1-3: Análisis de datos complejos ✓")
            print("CD2-3: Procesamiento matemático ✓") 
            print("AE1: Aplicación de teoría de información ✓")
            print("AE2: Optimización de preguntas ✓")
            print("Compromiso social: Educación ambiental ✓")
            
            print("\n🎯 ¡Sistema listo! Ahora puedes ejecutar:")
            print("   - entrenador.py para entrenar el sistema")
            print("   - adivinar.py para jugar")
        
    except KeyboardInterrupt:
        print("\nRegistro cancelado por el usuario")
    except Exception as e:
        print(f"\nError durante el registro: {e}")

if __name__ == '__main__':
    main()
