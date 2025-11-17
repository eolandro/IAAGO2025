from typing import List, Tuple, Optional
import sys

FILES = "abcdefgh"
RANKS = "12345678"
MOVES = [(2,1),(1,2),(-1,2),(-2,1),(-2,-1),(-1,-2),(1,-2),(2,-1)]

def parse_square(s: str) -> Tuple[int,int]:
    s = s.strip().lower()
    if len(s) != 2 or s[0] not in FILES or s[1] not in RANKS:
        raise ValueError("Entrada no válida. Formato: a1..h8")
    return FILES.index(s[0]), RANKS.index(s[1])

def fmt(coord: Tuple[int,int]) -> str:
    x,y = coord
    return f"{FILES[x]}{RANKS[y]}"

def in_board(x:int,y:int) -> bool:
    return 0 <= x < 8 and 0 <= y < 8

def knight_neighbors(x:int,y:int) -> List[Tuple[int,int]]:
    return [(x+dx, y+dy) for dx,dy in MOVES if in_board(x+dx, y+dy)]

# --- algoritmo: Warnsdorff + backtracking de respaldo ---
def warnsdorff_order(x:int,y:int, visited:set) -> List[Tuple[int,int]]:
    """Devuelve vecinos ordenados por número de futuros movimientos (heurística Warnsdorff)."""
    nbrs = knight_neighbors(x,y)
    nbrs = [n for n in nbrs if n not in visited]
    # contar grados
    nbrs.sort(key=lambda n: len([nn for nn in knight_neighbors(n[0], n[1]) if nn not in visited]))
    return nbrs

def find_tour(start:Tuple[int,int], want_closed:bool=True, max_attempts:int=5) -> Tuple[Optional[List[Tuple[int,int]]], bool]:
    """
    Intenta encontrar un tour completo (64 casillas).
    Devuelve (tour_list_or_None, is_cycle_bool).
    Primero intenta con heurística pura; si falla, hace backtracking recursivo con orden Warnsdorff.
    """
    sx, sy = start

    # intento rápido: aplicar Warnsdorff greedy
    def greedy():
        path = [(sx,sy)]
        visited = { (sx,sy) }
        for _ in range(63):
            x,y = path[-1]
            nbrs = warnsdorff_order(x,y, visited)
            if not nbrs:
                return None
            path.append(nbrs[0])
            visited.add(nbrs[0])
        return path

    tour = greedy()
    if tour:
        is_cycle = (start in knight_neighbors(tour[-1][0], tour[-1][1]))
        if want_closed and not is_cycle:
            # we'll allow non-closed but keep note
            return tour, False
        return tour, is_cycle

    # Si greedy falla, hacemos backtracking guiado por Warnsdorff
    sys.setrecursionlimit(10000)
    visited = set()
    path = []

    def backtrack(x:int,y:int, depth:int) -> Optional[List[Tuple[int,int]]]:
        path.append((x,y))
        visited.add((x,y))
        if depth == 64:
            # encontrado
            return path.copy()
        nbrs = warnsdorff_order(x,y, visited)
        # si quieres probar variaciones, podríamos mezclar órdenes; por ahora seguimos la lista
        for nx,ny in nbrs:
            res = backtrack(nx,ny, depth+1)
            if res is not None:
                return res
        # backtrack
        visited.remove((x,y))
        path.pop()
        return None

    tour = backtrack(sx, sy, 1)
    if tour is None:
        return None, False
    is_cycle = (start in knight_neighbors(tour[-1][0], tour[-1][1]))
    return tour, is_cycle

# --- impresión del tablero ---
def draw_board_from_path(path: List[Tuple[int,int]]):
    # construir matriz con 0..63 (o .)
    board = [[" ." for _ in range(8)] for __ in range(8)]
    for i,(x,y) in enumerate(path):
        board[y][x] = f"{i+1:2d}"
    print("\nTABLERO (fila 8 arriba):\n")
    for y in range(7, -1, -1):
        print(" ".join(board[y]) + f"   <- {y+1}")
    print(" a  b  c  d  e  f  g  h\n")

# --- programa principal ---
def main():
    try:
        start_str = input("Ingresa la casilla de inicio (ej: a1, d4): ").strip()
        start = parse_square(start_str)
    except Exception as e:
        print("Error:", e)
        return

    print("Buscando tour")
    tour, is_cycle = find_tour(start, want_closed=True)
    if tour is None:
        print("No se encontró un tour completo desde esa casilla (muy raro).")
        return

    print(f"\nSe encontró un tour de {len(tour)} casillas.")
    if is_cycle:
        print("Además: ¡es un ciclo cerrado! (la última casilla ataca a la inicial).")
    else:
        print("No es un ciclo cerrado (es un tour abierto válido).")

    # Mostrar movimientos ordenados
    print("\nRecorrido paso a paso:")
    for i,coord in enumerate(tour):
        print(f"{i+1:2d}: {fmt(coord)}")

    draw_board_from_path(tour)

main()
