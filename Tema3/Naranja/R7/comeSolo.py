def movimientos_posibles(tablero):
    return [
        (0, 1, 3), (0, 2, 5),
        (1, 3, 6), (1, 4, 8),
        (2, 4, 7), (2, 5, 9),
        (3, 1, 0), (3, 4, 5), (3, 6, 10), (3, 7, 12),
        (4, 7, 11), (4, 8, 13),
        (5, 2, 0), (5, 4, 3), (5, 8, 12), (5, 9, 14),
        (6, 3, 1), (6, 7, 8),
        (7, 4, 2), (7, 8, 9),
        (8, 4, 1), (8, 7, 6),
        (9, 5, 2), (9, 8, 7),
        (10, 6, 3), (10, 11, 12),
        (11, 7, 4), (11, 12, 13),
        (12, 7, 3), (12, 8, 5), (12, 11, 10), (12, 13, 14),
        (13, 8, 4), (13, 12, 11),
        (14, 9, 5), (14, 13, 12)
    ]

def dibujar_tablero(tablero):
    print("           ", tablero[0])
    print("         ", tablero[1], " ", tablero[2])
    print("       ", tablero[3], " ", tablero[4], " ", tablero[5])
    print("     ", tablero[6], " ", tablero[7], " ", tablero[8], " ", tablero[9])
    print("   ", tablero[10], " ", tablero[11], " ", tablero[12], " ", tablero[13], " ", tablero[14])
    print()

def resolver(tablero, path):
    if sum(tablero) == 1:
        return path
    for origen, salto, destino in movimientos_posibles(tablero):
        if tablero[origen] == 1 and tablero[salto] == 1 and tablero[destino] == 0:
            tablero[origen], tablero[salto], tablero[destino] = 0, 0, 1
            resultado = resolver(tablero, path + [(origen, salto, destino)])
            if resultado:
                return resultado
            tablero[origen], tablero[salto], tablero[destino] = 1, 1, 0
    return None

def tablero_posiciones():
    print("=== JUEGO DEL COME SOLO ===")
    print("Posiciones del tablero:\n")
    print("           0")
    print("         1   2")
    print("       3   4   5")
    print("     6   7   8   9")
    print("   10  11  12  13  14")
    print()

def main():
    tablero_posiciones()
    vacio = int(input("Por favor, ingrese la posición del espacio vacío inicial (0-14): "))
    
    tablero_inicial = [1] * 15
    tablero_inicial[vacio] = 0

    print("\nTablero inicial:\n")
    dibujar_tablero(tablero_inicial)

    solucion = resolver(tablero_inicial[:], [])
    if solucion:
        print("Solución encontrada:\n")
        tablero_actual = tablero_inicial[:]
        i = 1
        for mov in solucion:
            o, s, d = mov
            print(f"Movimiento {i}: {o} -> {d}")
            tablero_actual[o], tablero_actual[s], tablero_actual[d] = 0, 0, 1
            dibujar_tablero(tablero_actual)
            i += 1
    else:
        print("No se encontró solución desde esa posición inicial.")

if __name__ == "__main__":
    main()
