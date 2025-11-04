T = [[' '] * 4 for _ in range(4)] 
P0 = (0, 0) 

LP = [] 


for i in range(3, -1, -1):  
    for j in range(3, -1, -1):  
        LP.append((i, j))

def CP(P,PZ): 
    H = [] 
    for x in range(len(T)):
        for y in range(len(T[x])):
            if (x, y) == P or len(PZ) != 4:
                if T[x][y] != 'X':
                    for a in range(len(T)):
                        T[a][y] = 'X'
                    for b in range(len(T[x])):
                        T[x][b] = 'X'
                    c, d = x, y
                    while c >= 0 and d >= 0:
                        T[c][d] = 'X'
                        c -= 1
                        d -= 1
                    c, d = x, y
                    while c < len(T) and d < len(T):
                        T[c][d] = 'X'
                        c += 1
                        d += 1
                    c, d = x, y
                    while c >= 0 and d < len(T):
                        T[c][d] = 'X'
                        c -= 1
                        d += 1
                    c, d = x, y
                    while c < len(T) and d >= 0:
                        T[c][d] = 'X'
                        c += 1
                        d -= 1

                    if PZ:
                        FH = PZ.pop() 
                        T[x][y] = FH
                    UB = (x,y) 
                    H.append((UB,[F[:] for F in T])) 
                    if not PZ:
                        return H
C = 0 
while LP:
    CF = ['0'] * 4  
    PA = LP.pop() 
    R = CP(PA,CF) 
    if R:
        print("*---------------------------------*")
        print(f"|       Coordenada: {PA}        |")
        print("|       ¡Correcto!                |")
        print("*---------------------------------*\n")

        for PA, CO in R: 
            C = C + 1
            print(f"Ubicación {C} Coordenada: {PA}")
            
            print("|-----------------|")
            for L in CO:
                print("|  " + " | ".join(f"{E}" for E in L) + "  |") 
            print("|-----------------|")
            print()

    else:
        print(f"Coordenada {PA}: Sin solucion")
    T = [[' '] * 4 for _ in range(4)]
