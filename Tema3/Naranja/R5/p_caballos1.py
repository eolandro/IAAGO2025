def crear_tablero():
    tablero = []
    for i in range(3):
        fila = []
        for j in range(3):
            fila.append(".")
        tablero.append(fila)
    return tablero

def mostrar_tablero(tablero):
    for fila in tablero:
        print(" ".join(fila))
    print()

# Aviso al usuario
print("Por defecto, los caballos BLANCOS estarán en la parte superior del tablero.\n")

# Elección del sentido
print("¿En qué sentido se moverán?")
print("1. Horario")
print("2. Antihorario")
opcion_sentido = input("Elige 1 o 2: ")
print()

# Posiciones iniciales 
c1b_ini = (0, 0)
c2b_ini = (0, 2)
c1n_ini = (2, 0)
c2n_ini = (2, 2)

# Definición de recorridos según el sentido
if opcion_sentido == "1":  
    c1b_rec = [(0,0), (1,2), (2,0), (0,1), (2,2)]
    c2b_rec = [(0,2), (2,1), (0,0), (1,2), (2,0)]
    c1n_rec = [(2,0), (0,1), (2,2), (1,0), (0,2)]
    c2n_rec = [(2,2), (1,0), (0,2), (2,1), (0,0)]
else:  
    c1b_rec = [(0,0), (2,1), (0,2), (1,0), (2,2)]
    c2b_rec = [(0,2), (1,0), (2,2), (0,1), (2,0)]
    c1n_rec = [(2,0), (1,2), (0,0), (2,1), (0,2)]
    c2n_rec = [(2,2), (0,1), (2,0), (1,2), (0,0)]

# Simulación de estados 
for paso in range(5):
    tablero = crear_tablero()

    # Obtener posiciones actuales de cada caballo
    pos_c1b = c1b_rec[paso]
    pos_c2b = c2b_rec[paso]
    pos_c1n = c1n_rec[paso]
    pos_c2n = c2n_rec[paso]

    # Colocar caballos en el tablero
    tablero[pos_c1b[0]][pos_c1b[1]] = "B1"
    tablero[pos_c2b[0]][pos_c2b[1]] = "B2"
    tablero[pos_c1n[0]][pos_c1n[1]] = "N1"
    tablero[pos_c2n[0]][pos_c2n[1]] = "N2"

    # Mostrar el estado
    print("Estado", paso + 1)
    mostrar_tablero(tablero)
