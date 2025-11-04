from ruamel.yaml import YAML
import heapq

HV= [(-1, 0), (1, 0), (0, -1), (0, 1)]
D = [(-1, -1), (-1, 1), (1, -1), (1, 1)]
CL = HV + D

def R(A='T.yaml', R=5):
    yaml = YAML()
    with open(A, 'r') as F:
        D = yaml.load(F)
        L = D['T']

    def DL(X, Y, M):
        return 0 <= X < len(M) and 0 <= Y < len(M[0])

    def EV(X, Y, M):
        return DL(X, Y, M) and '1' not in M[X][Y]

    def EI_F(M):
        I, F = None, None
        for X in range(len(M)):
            for Y in range(len(M[0])):
                if 'B' in M[X][Y]:
                    I = (X, Y)
                if '2' in M[X][Y]:
                    F = (X, Y)
        return I, F

    def H(A, B):
        return abs(A[0] - B[0]) + abs(A[1] - B[1])

    def RC(DD, A):
        C = [A]
        while A in DD:
            A = DD[A]
            C.append(A)
        return C[::-1]

    def BC(M, I, F, R):
        if not I or not F:
            return None

        CP = [(H(I, F), I)]
        V = {I: 0}
        DD = {}

        while CP:
            PA, A = heapq.heappop(CP)

            if A == F:
                return RC(DD, A)

            X, Y = A
            for DX, DY in CL:
                VC = (X + DX, Y + DY)
                if EV(VC[0], VC[1], M):
                    CT = V[A] + 1 if A in V else float('inf')
                    if VC not in V or CT < V.get(VC, float('inf')):
                        V[VC] = CT
                        P = CT + H(VC, F) if H(A, F) > R else CT
                        heapq.heappush(CP, (P, VC))
                        DD[VC] = A

        return None

    I, F = EI_F(L)
    RUTA = BC(L, I, F, R)

    if RUTA is None:
        print('--------------------------------------------------------------------')
        print('                      NO HAY RUTA POSIBLES ')
        print('--------------------------------------------------------------------\n')
        print("El camino se a bloqueado\n")
        for FILA in L:
            print(FILA)
        print("\n")
    else:
        print('--------------------------------------------------------------------')
        print('                        RUTA COMPLETADA                              ')
        print('--------------------------------------------------------------------\n')
        for P, POS in enumerate(RUTA):
            X, Y = POS
            L[X][Y] = 'B'
            print(f"B= Boome  -  0= Espacios Vacios -  1= Obstaculos  -  2= Bomba")
            print(f"{P + 1}° Posición: {POS}:")
            for FILA in L:
                print(FILA)
            print("\n")
            L[X][Y] = '0'

        print("Ruta completa:\n",RUTA)
R()
