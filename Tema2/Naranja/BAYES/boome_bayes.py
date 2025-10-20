import random

FILAS = 10
COLUMNAS = 5
TOTAL = FILAS * COLUMNAS
MAX_DESACT = 3

# Precisión del detector
P_DET_BOMBA = 0.9   
P_DET_VACIA = 0.2  

def crear_matriz():
    # Crear matriz de ceros
    matriz = []
    for i in range(FILAS):
        fila = []
        for j in range(COLUMNAS):
            fila.append(0)
        matriz.append(fila)
    
    # Elegir posición aleatoria para la bomba 
    fila_bomba = random.randint(0, FILAS - 1)
    columna_bomba = random.randint(0, COLUMNAS - 1)
    
    # Colocar la bomba
    matriz[fila_bomba][columna_bomba] = 1
    
    return matriz, (fila_bomba, columna_bomba)

def crear_recorrido():
    posiciones = []
    
    for fila in range(FILAS):
        if fila % 2 == 0:
            # Filas pares: izquierda a derecha
            for columna in range(COLUMNAS):
                posiciones.append((fila, columna))
        else:
            # Filas impares: derecha a izquierda
            for columna in range(COLUMNAS - 1, -1, -1):
                posiciones.append((fila, columna))
    
    return posiciones

def calcular_probabilidad_bayes(p_bomba, p_no_bomba, p_detectar_bomba, p_detectar_vacia):
    
    probabilidad_detectar = (p_bomba * p_detectar_bomba) + (p_no_bomba * p_detectar_vacia)
    resultado = (p_detectar_bomba * p_bomba) / probabilidad_detectar
    return resultado

def usar_sensor(celda_tiene_bomba):
    
    if celda_tiene_bomba == 1:
        opciones = [1, 1, 1, 1, 1, 1, 1, 1, 1, 0]  
    else:
        opciones = [0, 0, 0, 0, 0, 0, 0, 0, 1, 1] 
    
    lectura = random.choice(opciones)
    return lectura 

def main():
    matriz, posicion_bomba = crear_matriz()
    print(f"Bomba colocada en {posicion_bomba}\n")
    
    
    recorrido = crear_recorrido()
    desactivadas = 0
    celdas_libres = TOTAL
    esta_vivo = True
    
    for fila, columna in recorrido:
        if not esta_vivo:
            break
        
        # Probabilidad inicial de que esta celda tenga la bomba
        probabilidad_bomba = 1.0 / celdas_libres
        celdas_libres = celdas_libres - 1
        
        valor_real = matriz[fila][columna]
        primera_lectura = usar_sensor(valor_real)
        
        if primera_lectura == 1:
            probabilidad_actual = probabilidad_bomba
            print(f"\n[{fila},{columna}] Detector: Posible Bomba")
            
            # Hacer tres comprobaciones bayesianas
            for revision in range(3):
                nueva_lectura = usar_sensor(valor_real)
                
                if nueva_lectura == 1:  # D+
                    probabilidad_no_bomba = 1.0 - probabilidad_actual
                    probabilidad_actual = calcular_probabilidad_bayes(
                        probabilidad_actual, 
                        probabilidad_no_bomba, 
                        P_DET_BOMBA, 
                        P_DET_VACIA
                    )
                    print(f"   Revisión {revision + 1}: D+ → P={probabilidad_actual * 100:.2f}%")
                else:  # D−
                    print(f"   Revisión {revision + 1}: D− (ignorando)")
            
            # Decidir si desactivar la bomba
            if probabilidad_actual >= 0.51 and desactivadas < MAX_DESACT:
                desactivadas = desactivadas + 1
                matriz[fila][columna] = 0
                print(f"→ Bomba desactivada ({fila},{columna})\n")
                
            else:
                print(f"→ Omitiendo bomba\n")
                
                if valor_real == 1:
                    print(f"Boome explotó en ({fila},{columna}) al pisar una bomba.\n")
                    
                    esta_vivo = False
                    break
        else:
            print(f"[{fila},{columna}] Detector: Vacío")
            if valor_real == 1:
                print(f"Boome explotó en ({fila},{columna}) al pisar una bomba que no detectó.\n")
                esta_vivo = False
                break
        
        if desactivadas >= MAX_DESACT:
            print("Límite de bombas desactivadas alcanzado.\n")
            break
    
    if esta_vivo:
        print("\nBoomie logró terminar el recorrido.")
    else:
        print("\nFin de la simulación: Boome explotó.")
    
    print("\n============ Resumen: ============")
    print(f"Casillas revisadas: {TOTAL - celdas_libres}")
    print(f"Bombas desactivadas: {desactivadas}")


main()