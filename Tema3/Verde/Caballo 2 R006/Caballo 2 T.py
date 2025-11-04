C = 64
L = 8

MC = [(2, 1), (1, 2), (-1, 2), (-2, 1),
                       (-2, -1), (-1, -2), (1, -2), (2, -1)]

def iT(t):
    for f in t:
        print(f)

def eV(x, y, t):
    return x >= 0 and y >= 0 and x < L and y < L and t[x][y] == -1

def cM(x, y, t):
    c = 0
    for Mx, My in MC:
        nX = x + Mx
        nY = y + My
        if eV(nX, nY, t):
            c += 1
    return c

def sM(x, y, t):
    m = 9
    b = (-1, -1)

    for Mx, My in MC:
        nX = x + Mx
        nY = y + My
        if eV(nX, nY, t):
            g = cM(nX, nY, t)
            if g < m:
                m = g
                b = (nX, nY)

    return b

def rC(x, y):
    t = [[-1 for _ in range(L)] for _ in range(L)]
    xi, yi = x, y

    t[xi][yi] = 0

    x, y = xi, yi

    for m in range(1, C):
        s = sM(x, y, t)
        if s == (-1, -1):
            print("No hay una solución")
            return False
        x, y = s
        t[x][y] = m

    print('- - - - - - - ¡COMPLETADO - - - - - - - \n')
    iT(t)
    return True

print('-------------------------------------')
print("            CABALLOS 2               ")
print('-------------------------------------\n')
print(f"Tablero: {L}x{L} = {C} casillas\n")

m = []
print("Tablero de coordenadas:\n")

for i in range(L):
    f = []
    for j in range(L):
        f.append(f'{i},{j}')
    m.append(f)

for f in m:
    print(f)

print()

c = input('Posición inicial (fila,columna): ')
print()
f, co = map(int, c.split(','))
rC(f, co)
