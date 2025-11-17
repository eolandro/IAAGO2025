def resolver_n_damas(n):
    tablero = [-1] * n
    soluciones = []
    backtracking(tablero, 0, n, soluciones)
    return soluciones

def es_seguro(tablero, fila_actual, columna_actual):
    for fila_anterior in range(fila_actual):
        columna_anterior = tablero[fila_anterior]
        
        if columna_anterior == columna_actual:
            return False
            
        if abs(fila_actual - fila_anterior) == abs(columna_actual - columna_anterior):
            return False
            
    return True

def backtracking(tablero, fila, n, soluciones):
    if fila == n:
        soluciones.append(list(tablero))
        return
        
    for columna in range(n):
        if es_seguro(tablero, fila, columna):
            tablero[fila] = columna
            backtracking(tablero, fila + 1, n, soluciones)
            # La vuelta atrás es implícita al sobrescribir o al terminar el stack.

def imprimir_solucion(solucion, n):
    tablero_str = ""
    for fila in range(n):
        linea = ""
        for col in range(n):
            if solucion[fila] == col:
                linea += " 1 "
            else:
                linea += " 0 "
        tablero_str += linea + "\n"
    return tablero_str

N = 4
soluciones = resolver_n_damas(N)

print(f"Se encontraron {len(soluciones)} soluciones")


for i, solucion in enumerate(soluciones):
    print(f"Solución {i+1}")
    print(imprimir_solucion(solucion, N))
    print("\n")
