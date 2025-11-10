import heapq
import json
with open('tablero.json', 'r') as arch:
    datos = json.load(arch)
    m = datos['matriz']

# Movimientos posiblkes arriba, abajo, izquierda, derecha
dirs = [(-1, 0), (1, 0), (0, -1), (0, 1)]

def es_val(x, y):
    return 0 <= x < len(m) and 0 <= y < len(m[0]) and 'X' not in m[x][y]

def puntos():
    ini = fin = None
    for i in range(len(m)):
        for j in range(len(m[0])):
            if 'B' in m[i][j]:
                ini = (i, j)
            elif '1' in m[i][j]:
                fin = (i, j)
    return ini, fin

def heur(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])

def camino(r_dijk=5):
    ini, fin = puntos()
    if not ini or not fin:
        return None

    abierta = []
    heapq.heappush(abierta, (heur(ini, fin), 0, ini))
    de_donde = {}
    g = {ini: 0}
    f = {ini: heur(ini, fin)}

    while abierta:
        nodo = heapq.heappop(abierta)  
        f_act = nodo[0]
        g_act = nodo[1]  
        act = nodo[2]  

        if act == fin:
            cam = []
            while act in de_donde:
                cam.append(act)
                act = de_donde[act]
            cam.append(ini)
            return cam[::-1]

        usar_dijk = heur(act, fin) <= r_dijk
        
        for dx, dy in dirs:
            nx, ny = act[0] + dx, act[1] + dy

            if not es_val(nx, ny) or (nx, ny) in g:
                continue

            g_nuevo = g_act + 1
            f_nuevo = g_nuevo if usar_dijk else g_nuevo + heur((nx, ny), fin)

            if f_nuevo < f.get((nx, ny), float('inf')):
                de_donde[(nx, ny)] = act
                g[(nx, ny)] = g_nuevo
                f[(nx, ny)] = f_nuevo
                heapq.heappush(abierta, (f_nuevo, g_nuevo, (nx, ny)))
    return None

ruta = camino()

if not ruta:
    print('-------No se encontro camino--------')
    print("Camino bloqueado\n")
    for fila in m:
        print(fila)
    print()
else:
    print('--------Boome seguira este camino--------')
    for paso, pos in enumerate(ruta):
        x, y = pos
        m[x][y] = 'B'
        print(f"moviendo a {paso + 1} - Posición: {pos}:")
        for fila in m:
            print(fila)
        print()
        m[x][y] = 'b'

    print("Recorrido de bomme", ruta)
