import cv2, numpy as np
from collections import deque
from config import C, F, A, X, Y, W, H

def e(P):
    Mc, Md = 1, float('inf')
    
    for I, Info in C.items():
        D = np.linalg.norm(P - Info["b"])
        if D < Md:
            Md, Mc = D, I
    
    return Mc, C[Mc]["n"]

def c(T):
    Ht, Wt = T.shape[:2]
    Cw, Ch = Wt // A, Ht // F
    
    G = []
    Est = {I: 0 for I in range(1, 7)}
    
    for Ff in range(F):
        R = []
        for Cc in range(A):
            Cx, Cy = int((Cc + 0.5) * Cw), int((Ff + 0.5) * Ch)
            
            M = [T[max(0, min(Ht-1, Cy + dy)), max(0, min(Wt-1, Cx + dx))]
                 for dy in (-1, 0, 1) for dx in (-1, 0, 1)]
            
            Pp = np.mean(M, axis=0).astype(int)
            
            Id, _ = e(Pp)
            
            R.append(Id)
            Est[Id] += 1
        
        G.append(R)
    
    return G

def g_sim(G, R, Ca, Co):
    S = np.array(G).copy()
    
    for I, J in R:
        S[I, J] = Co
    
    V = np.zeros((F, A), dtype=bool)
    Q = deque([(0, 0)])
    V[0, 0] = True
    N = set([(0, 0)])
    
    while Q:
        I, J = Q.popleft()
        for dI, dJ in ((0, 1), (1, 0), (0, -1), (-1, 0)):
            nI, nJ = I + dI, J + dJ
            if (0 <= nI < F and 0 <= nJ < A and not V[nI, nJ] 
                and S[nI, nJ] == Co):
                V[nI, nJ] = True
                Q.append((nI, nJ))
                N.add((nI, nJ))
    
    return len(N) - len(R)

def m(G):
    Tb = np.array(G)
    Ca = Tb[0, 0]
    
    V = np.zeros((F, A), dtype=bool)
    Q = deque([(0, 0)])
    V[0, 0] = True
    R = set([(0, 0)])
    
    while Q:
        I, J = Q.popleft()
        for dI, dJ in ((0, 1), (1, 0), (0, -1), (-1, 0)):
            nI, nJ = I + dI, J + dJ
            if (0 <= nI < F and 0 <= nJ < A and not V[nI, nJ] 
                and Tb[nI, nJ] == Ca):
                V[nI, nJ] = True
                Q.append((nI, nJ))
                R.add((nI, nJ))
    
    Bc = set()
    for I, J in R:
        for dI, dJ in ((0, 1), (1, 0), (0, -1), (-1, 0)):
            nI, nJ = I + dI, J + dJ
            if 0 <= nI < F and 0 <= nJ < A and (nI, nJ) not in R:
                Bc.add(Tb[nI, nJ])
    
    Mc, Mg = Ca, 0
    
    for Cc in Bc:
        if Cc == Ca:
            continue
        Gn = g_sim(Tb, R, Ca, Cc)
        if Gn > Mg:
            Mg, Mc = Gn, Cc
    
    return Mc, Mg, len(R)

def a(P):
    I = cv2.imread(P)
    if I is None:
        return None
    
    Ht, Wt = I.shape[:2]
    
    T = I[Y:Y+H, X:X+W]
    
    G = c(T)
    
    if not G:
        return None
    
    Mc, Ga, Ta = m(G)
    
    return G, Mc, Ga, Ta
