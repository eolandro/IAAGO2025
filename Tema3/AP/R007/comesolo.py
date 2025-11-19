MOVIMIENTOS = [
    (0, 1, 3), (3, 1, 0),
    (0, 2, 5), (5, 2, 0),
    (1, 3, 6), (6, 3, 1),
    (1, 4, 8), (8, 4, 1),
    (2, 4, 7), (7, 4, 2),
    (2, 5, 9), (9, 5, 2),
    (3, 4, 5), (5, 4, 3),
    (3, 6, 10), (10, 6, 3),
    (3, 7, 12), (12, 7, 3),
    (4, 7, 11), (11, 7, 4),
    (4, 8, 13), (13, 8, 4),
    (5, 8, 12), (12, 8, 5),
    (5, 9, 14), (14, 9, 5),
    (6, 7, 8), (8, 7, 6),
    (7, 8, 9), (9, 8, 7),
    (10,11,12), (12,11,10),
    (11,12,13), (13,12,11),
    (12,13,14), (14,13,12)
]


def resolver(tablero, movimientos_realizados):
    """Backtracking: intenta resolver el tablero."""
    if sum(tablero) == 1:
        return True  # solución encontrada

    for o, s, d in MOVIMIENTOS:
        # Validar movimiento: origen tiene ficha, salto tiene ficha, destino vacío
        if tablero[o] == 1 and tablero[s] == 1 and tablero[d] == 0:

            # hacer movimiento
            tablero[o] = 0
            tablero[s] = 0
            tablero[d] = 1
            movimientos_realizados.append((o, s, d))

            # llamada recursiva
            if resolver(tablero, movimientos_realizados):
                return True

            # deshacer (backtrack)
            tablero[o] = 1
            tablero[s] = 1
            tablero[d] = 0
            movimientos_realizados.pop()

    return False  # no hay solución por este camino


def imprimir_tablero(t):
    print()
    print("        ", t[0])
    print("       ", t[1], t[2])
    print("      ", t[3], t[4], t[5])
    print("     ", t[6], t[7], t[8], t[9])
    print("   ", t[10], t[11], t[12], t[13], t[14])
    print()


def main():
    pos = int(input("Ingrese la posición inicial vacía (0-14): "))

    # Crear tablero: todas fichas menos la inicial vacía
    tablero = [1] * 15
    tablero[pos] = 0

    print("\nTablero inicial:")
    imprimir_tablero(tablero)

    movimientos = []

    if resolver(tablero, movimientos):
        print("\nSOLUCIÓN ENCONTRADA")
        for i, (o, s, d) in enumerate(movimientos):
            print(f"{i+1}. {o} salta sobre {s} hacia {d}")
        print("\nTablero final:")
        imprimir_tablero(tablero)
    else:
        print("No existe solución desde esa posición.")


main()
