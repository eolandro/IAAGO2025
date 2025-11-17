# tablero inicial (puedes cambiar si quieres)
tablero = [
    ["1N", 0, "2N"],
    [   0, 0,    0],
    ["1B", 0, "2B"]
]

# anillo exterior en sentido horario (posiciones)
anillo = [(0,0),(0,1),(0,2),(1,2),(2,2),(2,1),(2,0),(1,0)]

# movimientos de caballo (delta)
def es_salto_valido(origen, destino):
    ar, ac = origen
    br, bc = destino
    dr, dc = abs(br - ar), abs(bc - ac)
    return (dr, dc) in {(1,2),(2,1)}

# imprimir tablero
def imprimir(t):
    for f in t:
        print(f)
    print()

# obtener las posiciones iniciales por color (sets)
initN = {(r,c) for r in range(3) for c in range(3)
         if isinstance(tablero[r][c], str) and tablero[r][c].endswith("N")}
initB = {(r,c) for r in range(3) for c in range(3)
         if isinstance(tablero[r][c], str) and tablero[r][c].endswith("B")}

# pedir sentido al usuario
sent = input("Sentido (h = horario, a = antihorario): ").strip().lower()
direccion = +1 if sent == 'h' or sent == 'horario' else -1

# función que avanza en el anillo según dirección
def next_in_ring(pos):
    i = anillo.index(pos)
    return anillo[(i + direccion) % len(anillo)]

# Buscar destino desde la posición actual
def buscar_destino_con_salto(pos_origen):
    origen = pos_origen
    actual = pos_origen
    for _ in range(len(anillo)):
        destino = next_in_ring(actual)
        r, c = destino
        # debe estar vacía y ser alcanzable desde la posición ORIGINAL
        if tablero[r][c] == 0 and es_salto_valido(origen, destino):
            return destino
        actual = destino
    return None

# obtener orden de piezas según anillo y dirección
def piezas_en_orden():
    seq = []
    for pos in (anillo if direccion==1 else list(reversed(anillo))):
        r,c = pos
        if tablero[r][c] != 0:
            seq.append(tablero[r][c])
    seen = set(); out = []
    for p in seq:
        if p not in seen:
            seen.add(p)
            out.append(p)
    return out

# condición de paro por inversión de colores
def invertido_por_color():
    curN = {(r,c) for r in range(3) for c in range(3)
            if isinstance(tablero[r][c], str) and tablero[r][c].endswith("N")}
    curB = {(r,c) for r in range(3) for c in range(3)
            if isinstance(tablero[r][c], str) and tablero[r][c].endswith("B")}
    return curN == initB and curB == initN

imprimir(tablero)

giro = 1
while True:
    print(f"\nGIRO #{giro}")

    orden_piezas = piezas_en_orden()

    for pieza in orden_piezas:
        # localizar pieza
        pos = None
        for r in range(3):
            for c in range(3):
                if tablero[r][c] == pieza:
                    pos = (r,c)
                    break
            if pos: break

        if pos is None:
            continue

        destino = buscar_destino_con_salto(pos)
        if destino is None:
            continue

        #aqui para ver si es un movimiento valido
        if not es_salto_valido(pos, destino):
            continue
        

        or_r, or_c = pos
        nr, nc = destino
        tablero[nr][nc] = pieza
        tablero[or_r][or_c] = 0
        print(f"Moviendo {pieza} de ({or_r},{or_c}) -> ({nr},{nc})")
        imprimir(tablero)

    if invertido_por_color():
        break

    giro += 1
