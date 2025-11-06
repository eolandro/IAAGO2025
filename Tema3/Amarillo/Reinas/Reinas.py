#Tablero vacio
mat = [['~'] * 4 for _ in range(4)]
cor = (0, 0)

cordena = []

#TABKERO DE 3-0.0-3 (4X4)
for fila in range(3, -1, -1):  
    for columna in range(3, -1, -1):  
        cordena.append((fila, columna))

def tablero(cord,pila):
    resultado = []
    for f in range(len(mat)):
        for c in range(len(mat[f])):
            if (f, c) == cord or len(pila) != 4:
                if mat[f][c] != 'X':
                    for fi in range(len(mat)):
                        mat[fi][c] = 'X'
                    for co in range(len(mat[f])):
                        mat[f][co] = 'X'
                    z, o = f, c
                    while z >= 0 and o >= 0:
                        mat[z][o] = 'X'
                        z -= 1
                        o -= 1
                    z, o = f, c
                    while z < len(mat) and o < len(mat):
                        mat[z][o] = 'X'
                        z += 1
                        o += 1
                    z, o = f, c
                    while z >= 0 and o < len(mat):
                        mat[z][o] = 'X'
                        z -= 1
                        o += 1
                    z, o = f, c
                    while z < len(mat) and o >= 0:
                        mat[z][o] = 'X'
                        z += 1
                        o -= 1

                    if pila:
                        elemento = pila.pop()
                        mat[f][c] = elemento
                    h = (f,c)
                    resultado.append((h,[fila[:] for fila in mat]))
                    if not pila:
                        return resultado
t = 0
while cordena:
    pila = ['O'] * 4
    coord = cordena.pop()
    O = tablero(coord,pila)
    if O:
        print(f"Cordenada{coord}:")
        print("    Solucion en tablero   \n")
       

        for coord, estado in O:
            t = t + 1
            print(f"Coordenada de REINA-{t} {coord}")
            for fila in estado:
                print(fila)
            print()
        t = 0
        
    else:
        print(f"Cordenada{coord}: No hay solucion")
    mat = [['~'] * 4 for _ in range(4)]
