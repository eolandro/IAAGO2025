from collections import Counter
from PIL import Image
import numpy as np
import subprocess
import time
import io
import math


colores = {
    1: (230, 58, 63),    
    2: (112, 140, 253),  
    3: (53, 156, 53),    
    4: (255, 206, 44),  
    5: (255, 111, 67),   
    6: (161, 60, 177)   
}


def detecolor(pixel):
    r, g, b = pixel
    midist = float('inf')
    color = 0
    
    for k, ref in colores.items():
        dr, dg, db = r - ref[0], g - ref[1], b - ref[2]
        dist = math.sqrt(dr*dr + dg*dg + db*db)
        if dist < midist:
            midist = dist
            color = k
    
    return color

def convimagen(img):

    w, h = img.size
    celw = w // 18
    celh = h // 18

    matriz = []
    for y in range(18):
        fila = []
        for x in range(18):
            px = img.crop((x*celw, y*celh, (x+1)*celw, (y+1)*celh))
            pixel = np.array(px).mean(axis=(0,1)) 
            fila.append(detecolor(pixel))
        matriz.append(fila)

    return matriz




adb = subprocess.Popen(
    ["adb", "shell"],
    stdin=subprocess.PIPE,
    stdout=subprocess.PIPE,
    stderr=subprocess.PIPE,
    text=True
    
)

def clic(x, y):
    comd = f"input tap {x} {y}\n"
    adb.stdin.write(comd)
    adb.stdin.flush()   
    time.sleep(0.30)

def movimintos(fila, col, posci, mat):

    moviX = [1,-1]
    moviY = [1,-1]
    posibles = []
    for dx in moviX:
        nuecol = col + dx
        if 0 <= nuecol < 18 and mat[fila][nuecol] != posci:  
            posibles.append((fila, nuecol))
    for dy in moviY:
        nuefil = fila + dy
        if 0 <= nuefil < 18 and mat[nuefil][col] != posci :
            posibles.append((nuefil, col))
          
        
           
    return posibles

def resolver(matr, ini,con):

    vec = {
    1: (200, 1900),  
    2: (300, 1900),  
    3: (500, 1900), 
    4: (700, 1900), 
    5: (800, 1900), 
    6: (900, 1900),  
}
    po = cordenadas(matr,0,0,ini)
   
    lis= [list(tupla) for tupla in po]
    pila = []
    for fila, col in lis:

        pila.append(movimintos(fila,col,ini, matr))


    pilasimp = [t for sublista in pila for t in sublista]

    pil = list(set(pilasimp))

    valores = [matr[fil][co] for fil, co in pil]
    conteo = Counter(valores)
    
    
    if not conteo:
        print("Fin del programa")
        return
    valrep = conteo.most_common(1)[0][0]
    if not lis:
        print("Fin del programa")
        return
    for fi, co in lis:
      matr[fi][co] = valrep
    valvec = vec.get(valrep)
    if valvec is None:
        print("Fin del programa")
        return
    
    clic(valvec[0], valvec[1])
    
    if con >= 31:
        print("Fin del programa")
        return
    resolver(matr, valrep, con + 1)

def cordenadas(mat, fila, col, val, vis=None):
    if vis is None:
        vis = set()  
    if fila < 0 or fila >= len(mat) or col < 0 or col >= len(mat[0]):
        return vis
    if mat[fila][col] != val or (fila, col) in vis:
        return vis
    vis.add((fila, col))
    movimientos = [(-1,0), (1,0), (0,-1), (0,1)]
    for df, dc in movimientos:
        cordenadas(mat, fila+df, col+dc, val, vis)

    return vis

def captura():
    raw = subprocess.check_output(["adb", "exec-out", "screencap", "-p"])
    return Image.open(io.BytesIO(raw))

def recortar(img):
    w, h = 939, 939 
    x = 70
    y = 727 
    area = (x, y, x + w, y + h)
    rec = img.crop(area)

    return rec


img = captura()
img2 = recortar(img)
img2 = img2.convert("RGB") 

matriz = convimagen(img2)

posini = matriz[0][0]
conta = 0

resolver(matriz,posini,conta)