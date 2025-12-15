import random
from collections import deque
import heapq
from typing import List, Tuple, Set, Optional
import time
import sys
import io

if sys.platform == 'win32':
    import os
    os.environ['PYTHONIOENCODING'] = 'utf-8'
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')


class OpenFloodBoard:
    """Representa el tablero del juego OpenFlood"""
    
    def __init__(self, width: int, height: int, num_colors: int, board: List[List[int]] = None):
        """Inicializa el tablero"""
        self.width = width
        self.height = height
        self.num_colors = num_colors
        self.board = board if board else []
        self.moves_made = 0
        self.solution = []
        
        if not self.board:
            self._generate_random_board()
    
    def _generate_random_board(self):
        """Genera un tablero aleatorio"""
        self.board = [[random.randint(0, self.num_colors - 1) 
                       for _ in range(self.width)] 
                      for _ in range(self.height)]
    
    def copy(self) -> 'OpenFloodBoard':
        """Retorna una copia profunda del tablero"""
        new_board = OpenFloodBoard(self.width, self.height, self.num_colors,
                                   [row[:] for row in self.board])
        new_board.moves_made = self.moves_made
        new_board.solution = self.solution[:]
        return new_board
    
    def get_flood_fill_cells(self) -> Set[Tuple[int, int]]:
        """
        Retorna el conjunto de celdas conectadas a la región inicial (esquina superior izquierda)
        que tienen el mismo color que la celda inicial.
        
        Returns:
            Conjunto de coordenadas (row, col) del mismo color conectado
        """
        original_color = self.board[0][0]
        visited = set()
        stack = [(0, 0)]
        
        # Encontrar todas las celdas conectadas del color original
        while stack:
            r, c = stack.pop()
            if (r, c) in visited:
                continue
            
            if r < 0 or r >= self.height or c < 0 or c >= self.width:
                continue
            
            if self.board[r][c] != original_color:
                continue
            
            visited.add((r, c))
            
            for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                nr, nc = r + dr, c + dc
                if 0 <= nr < self.height and 0 <= nc < self.width:
                    if (nr, nc) not in visited and self.board[nr][nc] == original_color:
                        stack.append((nr, nc))
        
        return visited
    
    def make_move(self, color: int) -> bool:
        """
        Realiza un movimiento (cambia el color en la región rellenada)
        
        Args:
            color: El color con el que rellenar
            
        Returns:
            True si el tablero cambió, False si ya era ese color
        """
        if self.board[0][0] == color:
            return False  # Ya es ese color, no hay cambio
        
        cells_to_fill = self.get_flood_fill_cells()
        
        if not cells_to_fill:
            return False
        
        for r, c in cells_to_fill:
            self.board[r][c] = color
        
        self.moves_made += 1
        self.solution.append(color)
        return True
    
    def is_solved(self) -> bool:
        """Verifica si todo el tablero es del mismo color"""
        target_color = self.board[0][0]
        for row in self.board:
            if any(cell != target_color for cell in row):
                return False
        return True
    
    def get_current_color(self) -> int:
        """Retorna el color actual en la esquina superior izquierda"""
        return self.board[0][0]
    
    def get_reachable_colors(self) -> Set[int]:
        """Retorna los colores vecinos a la región actual que se pueden alcanzar"""
        cells = self.get_flood_fill_cells()
        reachable = set()
        
        for r, c in cells:
            for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                nr, nc = r + dr, c + dc
                if 0 <= nr < self.height and 0 <= nc < self.width:
                    color = self.board[nr][nc]
                    if color != self.get_current_color():
                        reachable.add(color)
        
        return reachable
    
    def display(self):
        """Muestra el tablero en la consola"""
        color_map = {0: '🔴', 1: '🔵', 2: '🟢', 3: '🟡', 4: '🟠', 5: '🟣'}
        
        print("\n" + "="*50)
        for row in self.board:
            print(" ".join(color_map.get(cell, str(cell)) for cell in row))
        print("="*50)
        print(f"Movimientos realizados: {self.moves_made}")
        print(f"Resuelto: {'✓ SÍ' if self.is_solved() else '✗ NO'}")
    
    def __str__(self) -> str:
        """Representación en string del tablero"""
        result = []
        for row in self.board:
            result.append(" ".join(f"{cell}" for cell in row))
        return "\n".join(result)


class OpenFloodSolver:
    """Resuelve automáticamente los puzzles de OpenFlood"""
    
    def __init__(self, board: OpenFloodBoard):
        """
        Inicializa el solucionador
        
        Args:
            board: El tablero a resolver
        """
        self.board = board.copy()
        self.original_board = board.copy()
        self.solution_path = []
    
    def solve_bfs(self, max_moves: Optional[int] = None) -> List[int]:
        """
        Resuelve usando greedy
        
        Args:
            max_moves: Máximo número de movimientos permitidos
            
        Returns:
            Lista de colores para resolver el tablero
        """
        print("\n🔍 Iniciando búsqueda")
        start_time = time.time()
        
        queue = deque([(self.board.copy(), [])])
        visited = {self._board_to_hash(self.board)}
        moves_checked = 0
        
        while queue:
            current_board, path = queue.popleft()
            moves_checked += 1
            
            if current_board.is_solved():
                elapsed = time.time() - start_time
                print(f"✓ ¡Solución encontrada en {elapsed:.2f}s!")
                print(f"Movimientos evaluados: {moves_checked}")
                return path
            
            if max_moves and len(path) >= max_moves:
                continue
            
            # Probar todos los colores alcanzables
            for color in current_board.get_reachable_colors():
                new_board = current_board.copy()
                new_board.make_move(color)
                
                board_hash = self._board_to_hash(new_board)
                if board_hash not in visited:
                    visited.add(board_hash)
                    queue.append((new_board, path + [color]))
        
        elapsed = time.time() - start_time
        print(f"✗ No se encontró solución en {elapsed:.2f}s")
        return []
    
    def solve_greedy(self, iterations: int = 5) -> List[int]:
        """
        Resuelve usando algoritmo greedy con reintentos aleatorios
        
        Args:
            iterations: Número de intentos con diferentes estrategias
            
        Returns:
            Lista de colores para resolver el tablero
        """
        print("\nIniciando búsqueda Greedy...")
        start_time = time.time()
        
        best_solution = None
        best_moves = float('inf')
        
        for attempt in range(iterations):
            board = self.original_board.copy()
            solution = []
            moves = 0
            
            while not board.is_solved() and moves < 100:
                reachable = board.get_reachable_colors()
                
                if not reachable:
                    break
                
                # Estrategia: elegir el color que captura más celdas
                best_color = None
                best_count = 0
                
                for color in reachable:
                    test_board = board.copy()
                    test_board.make_move(color)
                    flood_cells = test_board.get_flood_fill_cells()
                    count = len(flood_cells)
                    
                    if count > best_count:
                        best_count = count
                        best_color = color
                
                if best_color is None:
                    # Fallback: elegir color aleatorio
                    best_color = random.choice(list(reachable))
                
                board.make_move(best_color)
                solution.append(best_color)
                moves += 1
            
            if board.is_solved() and moves < best_moves:
                best_moves = moves
                best_solution = solution
            
            print(f"  Intento {attempt + 1}/{iterations}: {moves} movimientos", end="")
            if board.is_solved():
                print(" ✓")
            else:
                print(" ✗")
        
        elapsed = time.time() - start_time
        
        if best_solution:
            print(f"\n✓ ¡Mejor solución encontrada en {elapsed:.2f}s!")
            print(f"Movimientos: {best_moves}")
            return best_solution
        else:
            print(f"\n✗ No se encontró solución")
            return []
    
    def _board_to_hash(self, board: OpenFloodBoard) -> str:
        """Convierte el tablero a un hash para visitados"""
        return str(board.board)
    
    def solve_astar(self, max_time: float = 60.0) -> List[int]:
        """
        Resuelve usando A* (mucho más rápido que BFS con buena heurística)
        
        Args:
            max_time: Máximo tiempo en segundos
            
        Returns:
            Lista de colores para resolver el tablero
        """
        import heapq
        
        print("\n Iniciando búsqueda A*...")
        start_time = time.time()
        
        def heuristic(board: OpenFloodBoard) -> int:
            """Heurística: número de colores diferentes en el tablero"""
            colors = set()
            for row in board.board:
                for cell in row:
                    colors.add(cell)
            return len(colors) - 1  # -1 porque queremos un solo color
        
        # (f_score, counter, board, path)
        initial_h = heuristic(self.board)
        heap = [(initial_h, 0, self.board.copy(), [])]
        visited = {self._board_to_hash(self.board)}
        counter = 1
        nodes_explored = 0
        
        while heap:
            if time.time() - start_time > max_time:
                print(f"[!] Tiempo máximo ({max_time}s) excedido")
                break
            
            f_score, _, current_board, path = heapq.heappop(heap)
            nodes_explored += 1
            
            if nodes_explored % 100 == 0:
                print(f"  Explorados: {nodes_explored} nodos, mejor f={f_score}, profundidad={len(path)}")
            
            if current_board.is_solved():
                elapsed = time.time() - start_time
                print(f"✓ ¡Solución encontrada en {elapsed:.2f}s!")
                print(f"  Nodos explorados: {nodes_explored}")
                return path
            
            # Probar todos los colores alcanzables
            for color in current_board.get_reachable_colors():
                new_board = current_board.copy()
                new_board.make_move(color)
                
                board_hash = self._board_to_hash(new_board)
                if board_hash not in visited:
                    visited.add(board_hash)
                    
                    g = len(path) + 1  # costo real
                    h = heuristic(new_board)  # heurística
                    f = g + h  # f = g + h
                    
                    heapq.heappush(heap, (f, counter, new_board, path + [color]))
                    counter += 1
        
        elapsed = time.time() - start_time
        print(f"✗ No se encontró solución en {elapsed:.2f}s ({nodes_explored} nodos)")
        return []
    
    def solve_ida_star(self, max_time: float = 60.0) -> List[int]:
        """
        Resuelve usando IDA* (Iterative Deepening A*)
        Mucho más rápido que BFS y garantiza solución óptima
        
        Args:
            max_time: Máximo tiempo en segundos
            
        Returns:
            Lista de colores para resolver el tablero
        """
        print("\n⭐ Iniciando búsqueda IDA*...")
        start_time = time.time()
        
        def heuristic(board: OpenFloodBoard) -> int:
            """Heurística: número de colores diferentes"""
            colors = set()
            for row in board.board:
                for cell in row:
                    colors.add(cell)
            return len(colors) - 1
        
        def search(board: OpenFloodBoard, path: List[int], g: int, threshold: int) -> Tuple[List[int], int]:
            """Búsqueda DFS con límite f"""
            f = g + heuristic(board)
            
            if f > threshold:
                return None, f
            
            if board.is_solved():
                return path, f
            
            min_threshold = float('inf')
            
            for color in board.get_reachable_colors():
                new_board = board.copy()
                new_board.make_move(color)
                
                result, new_threshold = search(new_board, path + [color], g + 1, threshold)
                
                if result is not None:
                    return result, new_threshold
                
                min_threshold = min(min_threshold, new_threshold)
            
            return None, min_threshold
        
        # IDA* - aumentar el umbral iterativamente
        threshold = heuristic(self.board)
        iteration = 0
        
        while time.time() - start_time < max_time:
            iteration += 1
            print(f"  Iteración {iteration}: threshold={threshold}")
            
            result, next_threshold = search(self.board.copy(), [], 0, threshold)
            
            if result is not None:
                elapsed = time.time() - start_time
                print(f"✓ ¡Solución encontrada en {elapsed:.2f}s!")
                return result
            
            if next_threshold == float('inf'):
                break
            
            threshold = next_threshold
        
        elapsed = time.time() - start_time
        print(f"✗ No se encontró solución en {elapsed:.2f}s")
        return []
    
    def solve_iddfs(self, max_time: float = 240.0) -> List[int]:
        """
        Resuelve usando Greedy inteligente + IDDFS como fallback
        Cada uno maneja su propio tiempo independiente
        
        Args:
            max_time: Máximo tiempo en segundos para cada estrategia
            
        Returns:
            Lista de colores para resolver el tablero
        """
        print("\n🔍 Iniciando búsqueda híbrida (Greedy + IDDFS)...")
        
        # PASO 1: Intentar con Greedy inteligente paralelo
        print(f"  [1/2] Intentando Greedy inteligente ({max_time:.0f}s)...")
        greedy_start = time.time()
        
        def analyze_color_clusters(board):
            """Analiza concentraciones de colores"""
            color_counts = {}
            for row in board.board:
                for cell in row:
                    color_counts[cell] = color_counts.get(cell, 0) + 1
            return color_counts
        
        initial_counts = analyze_color_clusters(self.board)
        
        print(f"      Colores iniciales: {len(initial_counts)}")
        print(f"      Distribución: {sorted(initial_counts.values(), reverse=True)}")
        
        def greedy_step(board, color_counts):
            """Elige el mejor color por densidad"""
            reachable = board.get_reachable_colors()
            if not reachable:
                return None
            return max(reachable, key=lambda c: color_counts.get(c, 0))
        
        import threading
        
        best_greedy_solution = []
        best_greedy_length = 32
        solution_lock = threading.Lock()
        
        def worker_greedy():
            nonlocal best_greedy_solution, best_greedy_length
            
            for attempt in range(50):
                elapsed = time.time() - greedy_start
                if elapsed > max_time:
                    break
                
                board = self.board.copy()
                solution = []
                
                while not board.is_solved():
                    color_counts = analyze_color_clusters(board)
                    color = greedy_step(board, color_counts)
                    
                    if color is None:
                        break
                    
                    board.make_move(color)
                    solution.append(color)
                    
                    if len(solution) > 31:
                        break
                
                if board.is_solved() and len(solution) <= 31:
                    with solution_lock:
                        if len(solution) < best_greedy_length:
                            best_greedy_solution = solution
                            best_greedy_length = len(solution)
                            elapsed = time.time() - greedy_start
                            print(f"      ✓ Intento {attempt + 1}: {len(solution)} movimientos en {elapsed:.2f}s")
        
        # Ejecutar Greedy con threads
        num_threads = 4
        threads = []
        for i in range(num_threads):
            t = threading.Thread(target=worker_greedy, daemon=True)
            t.start()
            threads.append(t)
        
        for t in threads:
            t.join(timeout=max_time)
        
        if best_greedy_solution and len(best_greedy_solution) <= 31:
            elapsed = time.time() - greedy_start
            print(f"✓ ¡Solución Greedy encontrada: {len(best_greedy_solution)} movimientos en {elapsed:.2f}s!")
            return best_greedy_solution
        
        # PASO 2: Si Greedy no encontró, intentar IDDFS con su propio tiempo independiente
        print(f"  [2/2] Greedy no encontró, intentando IDDFS ({max_time:.0f}s)...")
        
        iddfs_start = time.time()
        
        def dfs_limited(board, path, depth, max_depth):
            """DFS con límite de profundidad"""
            if board.is_solved():
                return path
            
            if depth > max_depth:
                return None
            
            for color in board.get_reachable_colors():
                if time.time() - iddfs_start > max_time:
                    return None
                
                new_board = board.copy()
                new_board.make_move(color)
                
                result = dfs_limited(new_board, path + [color], depth + 1, max_depth)
                if result is not None:
                    return result
            
            return None
        
        # Buscar con profundidad decreciente (desde 31 hacia 27)
        # Soluciones típicas están entre 27-31 movimientos
        for max_depth in range(31, 26, -1):
            if time.time() - iddfs_start > max_time:
                break
            
            print(f"      Buscando solución con máximo {max_depth} movimientos...")
            result = dfs_limited(self.board.copy(), [], 0, max_depth)
            
            if result is not None:
                elapsed = time.time() - iddfs_start
                print(f"✓ ¡Solución IDDFS encontrada: {len(result)} movimientos en {elapsed:.2f}s!")
                return result
        
        return []
    
    def apply_solution(self, solution: List[int]) -> bool:
        """
        Aplica una solución al tablero y la visualiza
        
        Args:
            solution: Lista de colores a aplicar en orden
            
        Returns:
            True si la solución resolvió el tablero
        """
        if not solution:
            print("No hay solución que aplicar")
            return False
        
        print("\n📋 APLICANDO SOLUCIÓN:")
        print("=" * 50)
        
        for i, color in enumerate(solution, 1):
            self.board.make_move(color)
            print(f"Movimiento {i}: Color {color}")
        
        print("=" * 50)
        self.board.display()
        
        return self.board.is_solved()
    
    def solve_fast(self, max_time: float = 30.0) -> List[int]:
        """
        Resuelve muy rápido usando múltiples estrategias greedy en paralelo
        Explora diversas opciones simultáneamente para encontrar una buena solución rápidamente
        
        Args:
            max_time: Máximo tiempo en segundos
            
        Returns:
            Lista de movimientos de color (secuencia de colores a tocar)
        """
        print("\n⚡ Iniciando búsqueda RÁPIDA con estrategias paralelas...")
        start_time = time.time()
        
        best_solution = None
        best_moves = float('inf')
        
        # Ejecutar múltiples greedy con diferentes estrategias simultáneamente
        try:
            from multiprocessing import Pool, cpu_count
            
            def solve_greedy_variant(num_iterations):
                """Ejecuta greedy con cierta cantidad de iteraciones"""
                board = self.board.copy()
                for _ in range(num_iterations):
                    if board.is_solved():
                        return board.solution.copy(), board.moves_made
                    
                    reachable = board.get_reachable_colors()
                    if not reachable:
                        break
                    
                    best_color = None
                    best_count = 0
                    
                    for color in reachable:
                        test_board = board.copy()
                        test_board.make_move(color)
                        flood_cells = test_board.get_flood_fill_cells()
                        count = len(flood_cells)
                        
                        if count > best_count:
                            best_count = count
                            best_color = color
                    
                    if best_color is None:
                        best_color = random.choice(list(reachable))
                    
                    board.make_move(best_color)
                
                return board.solution.copy(), board.moves_made
            
            # Ejecutar en paralelo con diferentes números de iteraciones
            num_workers = min(cpu_count(), 4)
            iterations_list = [10, 15, 20, 25, 30][:num_workers]
            
            with Pool(num_workers) as pool:
                results = pool.map(solve_greedy_variant, iterations_list, chunksize=1)
                
                for solution, moves in results:
                    elapsed = time.time() - start_time
                    if elapsed > max_time:
                        break
                    
                    if moves < best_moves:
                        best_moves = moves
                        best_solution = solution
                        print(f"  ✓ Encontrado: {moves} movimientos")
        except:
            # Fallback a single-threaded si hay error en multiprocessing
            print("  [Fallback a modo single-threaded]")
            best_solution = self.solve_greedy(iterations=30)
            best_moves = len(best_solution) if best_solution else float('inf')
        
        elapsed = time.time() - start_time
        
        if best_solution:
            print(f"⚡ ¡Mejor solución: {best_moves} movimientos en {elapsed:.2f}s!")
            return best_solution
        
        print(f"✗ No se encontró solución en {elapsed:.2f}s")
        return []
    
    def get_difficulty_level(self) -> int:
        """Estima el nivel de dificultad (movimientos aproximados esperados)"""
        # Heurística simple: contar número de colores y tamaño del tablero
        unique_colors = len(set(cell for row in self.board.board for cell in row))
        return unique_colors + (self.board.height * self.board.width) // 100


def main():
    """Función principal de demostración"""
    print("╔════════════════════════════════════════════════════╗")
    print("║         OPENFLOOD SOLVER - IA PROJECT             ║")
    print("║      Resolvedor automático del juego OpenFlood     ║")
    print("╚════════════════════════════════════════════════════╝")
    
    # Crear un tablero de prueba
    width, height = 5, 5
    num_colors = 4
    
    print(f"\n📊 Parámetros del tablero:")
    print(f"   Dimensiones: {width}x{height}")
    print(f"   Colores: {num_colors}")
    
    board = OpenFloodBoard(width, height, num_colors)
    
    print("\n📺 TABLERO INICIAL:")
    board.display()
    
    # Resolver
    solver = OpenFloodSolver(board)
    
    # Usar greedy para tableros (más rápido y práctico)
    solution = solver.solve_greedy(iterations=20)
    
    # Mostrar solución
    if solution:
        solver.apply_solution(solution)
        print(f"\n✨ SOLUCIÓN COMPLETA EN {len(solution)} MOVIMIENTOS")
        print(f"   Secuencia: {' → '.join(str(c) for c in solution)}")
    else:
        print("\n❌ No se pudo encontrar una solución")


if __name__ == "__main__":
    main()
