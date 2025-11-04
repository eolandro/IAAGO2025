class N:
    def __init__(self, T, M=None, P=None):
        self.T = T
        self.M = M
        self.P = P
        self.H = []

    def A(self, n):
        self.H.append(n)

class TP:
    def __init__(self, I):
        self.T = [[1 for a in range(i + 1)] for i in range(5)]
        self.T[I[0]][I[1]] = 0
        self.R = N(self.T)
        self.M = None
        self.V = set()

    def G(self, n):
        t = n.T
        L = []
        D = [(0, 2), (0, -2), (2, 0), (-2, 0), (2, 2), (-2, -2)]

        for i in range(len(t)):
            for j in range(len(t[i])):
                if t[i][j] == 1:
                    for d in D:
                        dx = d[0]
                        dy = d[1]
                        if self.VM(t, i, j, dx, dy):
                            NT = self.RM(t, i, j, dx, dy)
                            L.append((NT, (i, j, i + dx, j + dy)))
        return L

    def VM(self, t, x, y, dx, dy):
        if (0 <= x + dx < len(t) and
                0 <= y + dy < len(t[x + dx]) and
                t[x][y] == 1 and
                t[x + dx][y + dy] == 0 and
                t[x + dx // 2][y + dy // 2] == 1):
            return True
        return False

    def RM(self, t, x, y, dx, dy):
        NT = [fila.copy() for fila in t]
        NT[x][y] = 0
        NT[x + dx][y + dy] = 1
        NT[x + dx // 2][y + dy // 2] = 0
        return NT

    def GA(self):
        NA = [self.R]
        self.V.add(str(NA[0].T))

        while NA:
            NS = []

            for n in NA:
                for NT, M in self.G(n):
                    TS = str(NT)
                    if TS not in self.V:
                        H = N(NT, M, n)
                        n.A(H)
                        NS.append(H)
                        self.V.add(TS)

                        if self.EM(NT):
                            self.M = H
                            return
            NA = NS

    def EM(self, t):
        C = sum(fila.count(1) for fila in t)
        return C == 1

    def IS(self):
        if not self.M:
            print('Sin solución')
            return

        C = []
        NA = self.M

        while NA:
            C.append((NA.T, NA.M))
            NA = NA.P

        for NM, (T, M) in enumerate(reversed(C[:-1]), 1):
            if M:
                D = (M[0], M[1])
                A = (M[2], M[3])
                print(f'\nMovimiento {NM}: {D} a {A}')
                self.IT(T)

    def IT(self, t):
        for i, F in enumerate(t):
            print(' ' * (4 - i) + ' '.join(['0' if c == 1 else '_' for c in F]))


def IT(n):
    for i in range(n):
        print('   ' * (n - i - 1), end='')
        for j in range(i + 1):
            print(f'{i},{j}', end='   ')
        print()


def main():
    print("\n* - - - - JUEGO  COME SOLO - - - - *\n")
    IT(5)
    E = input('\nColoca una posicion para comenzar Ejem: (fila, columna): ')
    PI = tuple(map(int, E.strip('()').split(',')))

    J = TP(PI)
    print('* - - - - - - - - -*')
    print('Solución encontrada')
    print('* - - - - - - - - -*')
    print("Estado inicial del tablero:")
    J.IT(J.T)
    J.GA()
    J.IS()


if __name__ == '__main__':
    main()
