

import pyautogui
import numpy as np
from PIL import ImageGrab
import cv2
import time
import json
import os
from typing import Optional, List, Dict, Tuple
from hamiltonian_solver import HamiltonFloodBoard, HamiltonFloodSolver


class GameDetector:
    """Detector de tablero y botones"""
    
    def __init__(self):
        self.drawing = False
        self.start_point = None
        self.end_point = None
        self.rect_points = []
        self.color_calibration = self._load_calibration()
    
    def _load_calibration(self) -> Dict:
        calib_file = "color_calibration.json"
        default_colors = {
            0: (237, 52, 55),       # Rojo
            1: (68, 138, 255),      # Azul
            2: (76, 175, 80),       # Verde
            3: (255, 193, 7),       # Amarillo
            4: (255, 152, 51),      # Naranja
            5: (171, 71, 188),      # Morado
        }
        
        if os.path.exists(calib_file):
            try:
                with open(calib_file, 'r') as f:
                    loaded = json.load(f)
                    calibration = {int(k): tuple(v) for k, v in loaded.items()}
                    print(f"[+] Calibración cargada desde {calib_file}")
                    return calibration
            except Exception as e:
                print(f"[-] Error cargando calibración: {e}")
                pass
        
        return default_colors
    
    def _save_calibration(self):
        """Guarda la calibración actual en archivo"""
        calib_file = "color_calibration.json"
        to_save = {str(k): list(v) for k, v in self.color_calibration.items()}
        with open(calib_file, 'w') as f:
            json.dump(to_save, f, indent=2)
        print(f"[+] Calibración guardada en {calib_file}")
    
    def mouse_callback(self, event, x, y, flags, param):
        """Callback para detectar clics del mouse"""
        if event == cv2.EVENT_LBUTTONDOWN:
            self.drawing = True
            self.start_point = (x, y)
        elif event == cv2.EVENT_MOUSEMOVE and self.drawing:
            self.end_point = (x, y)
        elif event == cv2.EVENT_LBUTTONUP:
            self.drawing = False
            self.end_point = (x, y)
            if self.start_point and self.end_point:
                x1, y1 = self.start_point
                x2, y2 = self.end_point
                if x2 < x1:
                    x1, x2 = x2, x1
                if y2 < y1:
                    y1, y2 = y2, y1
                self.rect_points.append((x1, y1, x2, y2))
                print(f"[+] Región marcada: ({x1}, {y1}) a ({x2}, {y2})")
    
    def mark_regions(self, img: np.ndarray) -> tuple:
        """Permite marcar el tablero y los botones con el mouse"""
        display = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
        window_name = "Hamilton Flood Region Marker"
        cv2.namedWindow(window_name)
        cv2.setMouseCallback(window_name, self.mouse_callback)
        
        print("\n" + "="*60)
        print("[1] Marca el TABLERO: dibuja un rectángulo alrededor")
        print("[2] Presiona ENTER cuando termines")
        print("[3] Luego marca el área de los BOTONES")
        print("="*60)
        
        self.rect_points = []
        
        # Marcar tablero
        print("\n[!] Dibuja un rectángulo alrededor del TABLERO...")
        print("    Haz clic y arrastra para dibujar")
        
        while len(self.rect_points) < 1:
            display = cv2.cvtColor(img, cv2.COLOR_RGB2BGR).copy()
            
            if self.drawing and self.start_point and self.end_point:
                cv2.rectangle(display, self.start_point, self.end_point, (0, 255, 0), 2)
                cv2.putText(display, "Tablero", (self.start_point[0] + 10, self.start_point[1] - 10),
                           cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
            
            for i, (x1, y1, x2, y2) in enumerate(self.rect_points):
                cv2.rectangle(display, (x1, y1), (x2, y2), (0, 255, 0), 3)
                cv2.putText(display, f"Tablero", (x1 + 10, y1 - 10),
                           cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
            
            cv2.imshow(window_name, display)
            key = cv2.waitKey(1) & 0xFF
            if key == 13:
                if len(self.rect_points) > 0:
                    break
        
        board_region = self.rect_points[0]
        self.rect_points = []
        
        # Marcar botones
        print("\n[!] Dibuja un rectángulo alrededor de los BOTONES...")
        print("    Haz clic y arrastra para dibujar")
        
        while len(self.rect_points) < 1:
            display = cv2.cvtColor(img, cv2.COLOR_RGB2BGR).copy()
            
            x1, y1, x2, y2 = board_region
            cv2.rectangle(display, (x1, y1), (x2, y2), (0, 255, 0), 2)
            cv2.putText(display, "Tablero", (x1 + 10, y1 - 10),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)
            
            if self.drawing and self.start_point and self.end_point:
                cv2.rectangle(display, self.start_point, self.end_point, (255, 0, 0), 2)
                cv2.putText(display, "Botones", (self.start_point[0] + 10, self.start_point[1] - 10),
                           cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)
            
            for i, (x1, y1, x2, y2) in enumerate(self.rect_points):
                cv2.rectangle(display, (x1, y1), (x2, y2), (255, 0, 0), 3)
                cv2.putText(display, f"Botones", (x1 + 10, y1 - 10),
                           cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)
            
            cv2.imshow(window_name, display)
            key = cv2.waitKey(1) & 0xFF
            if key == 13:
                if len(self.rect_points) > 0:
                    break
        
        buttons_region = self.rect_points[0]
        
        cv2.destroyAllWindows()
        
        print(f"\n[+] Tablero: {board_region}")
        print(f"[+] Botones: {buttons_region}")
        
        return board_region, buttons_region
    
    def capture_screen(self) -> np.ndarray:
        """Captura la pantalla como array numpy RGB - preserva colores exactos"""
        screenshot = ImageGrab.grab()
        img = np.array(screenshot)
        return img
    
    def detect_board_colors(self, img: np.ndarray, board_region: tuple, grid_size: int = 18) -> Optional[List[List[int]]]:
        """Detecta colores del tablero ignorando bordes de celdas"""
        if board_region is None:
            print("[-] No se proporcionó región del tablero")
            return None
        
        x1, y1, x2, y2 = board_region
        board_img = img[y1:y2, x1:x2]
        
        height, width = board_img.shape[:2]
        
        print(f"[*] Tablero: {grid_size}x{grid_size}")
        print(f"[*] Región exacta: {width}x{height}")
        
        board = []
        rgb_samples = {i: [] for i in range(6)}
        
        for row in range(grid_size):
            board_row = []
            y_start = int(row * height / grid_size)
            y_end = int((row + 1) * height / grid_size)
            
            for col in range(grid_size):
                x_start = int(col * width / grid_size)
                x_end = int((col + 1) * width / grid_size)
                
                margin_x = max(1, (x_end - x_start) // 5)
                margin_y = max(1, (y_end - y_start) // 5)
                
                center_x_start = x_start + margin_x
                center_x_end = x_end - margin_x
                center_y_start = y_start + margin_y
                center_y_end = y_end - margin_y
                
                cell_center = board_img[center_y_start:center_y_end, center_x_start:center_x_end]
                
                if cell_center.size == 0:
                    board_row.append(2)
                    continue
                
                avg_color = cv2.mean(cell_center)[:3]
                color_rgb = (int(avg_color[2]), int(avg_color[1]), int(avg_color[0]))
                
                color_id = self._classify_color(color_rgb)
                board_row.append(color_id)
                rgb_samples[color_id].append(color_rgb)
            
            board.append(board_row)
        
        self._print_color_stats(rgb_samples)
        
        return board
    
    def _print_color_stats(self, rgb_samples: Dict):
        """Imprime estadísticas de los colores detectados"""
        names = ["Rojo", "Azul", "Verde", "Amarillo", "Naranja", "Morado"]
        print("\n[*] ESTADÍSTICAS DE COLORES DETECTADOS:")
        print("=" * 70)
        
        for color_id in range(6):
            samples = rgb_samples[color_id]
            if not samples:
                print(f"  {color_id} - {names[color_id]:10s}: NO DETECTADO")
                continue
            
            avg_r = sum(r for r, g, b in samples) // len(samples)
            avg_g = sum(g for r, g, b in samples) // len(samples)
            avg_b = sum(b for r, g, b in samples) // len(samples)
            
            min_r = min(r for r, g, b in samples)
            max_r = max(r for r, g, b in samples)
            min_g = min(g for r, g, b in samples)
            max_g = max(g for r, g, b in samples)
            min_b = min(b for r, g, b in samples)
            max_b = max(b for r, g, b in samples)
            
            print(f"  {color_id} - {names[color_id]:10s}: {len(samples):3d} muestras -> RGB({avg_r}, {avg_g}, {avg_b})")
            print(f"      Rangos: R[{min_r}-{max_r}]  G[{min_g}-{max_g}]  B[{min_b}-{max_b}]")
        
        print("=" * 70)
    
    def _classify_color(self, rgb: Tuple[int, int, int]) -> int:
        """Clasifica RGB directamente por distancia a colores conocidos"""
        r, g, b = rgb
        colors = self.color_calibration
        
        min_dist = float('inf')
        best = 2
        distances = {}
        
        for cid, (cr, cg, cb) in colors.items():
            dist = ((r - cr)**2 + (g - cg)**2 + (b - cb)**2) ** 0.5
            distances[cid] = dist
            if dist < min_dist:
                min_dist = dist
                best = cid
        
        return best
    
    def find_color_buttons_in_region(self, img: np.ndarray, buttons_region: tuple) -> Dict[int, Tuple[int, int]]:
        """Encuentra los botones de color dividiendo la región proporcionalmente"""
        if buttons_region is None:
            return {}
        
        x1, y1, x2, y2 = buttons_region
        width = x2 - x1
        height = y2 - y1
        num_buttons = 6
        
        buttons = {}
        
        for btn_idx in range(num_buttons):
            x_start = int(btn_idx * width / num_buttons)
            x_end = int((btn_idx + 1) * width / num_buttons)
            
            cx = x1 + x_start + (x_end - x_start) // 2
            cy = y1 + height // 2
            
            buttons[btn_idx] = (cx, cy)
        
        return buttons
    
    def detect_buttons_colors(self, img: np.ndarray, buttons_region: tuple) -> List[int]:
        """Detecta los colores de los 6 botones en la región especificada"""
        if buttons_region is None:
            return []
        
        button_samples = self._get_button_samples(img, buttons_region)
        if not button_samples:
            return []
        
        button_colors = []
        for rgb in button_samples:
            color_id = self._classify_color(rgb)
            button_colors.append(color_id)
            names = ["Rojo", "Azul", "Verde", "Amarillo", "Naranja", "Morado"]
            print(f"[DEBUG] Botón {len(button_colors)-1}: RGB{rgb} -> Color {color_id} ({names[color_id]})")
        
        return button_colors
    
    def _get_button_samples(self, img: np.ndarray, buttons_region: tuple) -> List[tuple]:
        """Extrae el color RGB de cada uno de los 6 botones"""
        if buttons_region is None:
            return []
        
        x1, y1, x2, y2 = buttons_region
        buttons_img = img[y1:y2, x1:x2]
        
        height, width = buttons_img.shape[:2]
        num_buttons = 6
        
        button_samples = []
        
        for btn in range(num_buttons):
            x_start = int(btn * width / num_buttons)
            x_end = int((btn + 1) * width / num_buttons)
            
            margin_x = max(2, int((x_end - x_start) * 0.3))
            margin_y = max(2, int(height * 0.3))
            
            center_x_start = x_start + margin_x
            center_x_end = x_end - margin_x
            center_y_start = margin_y
            center_y_end = height - margin_y
            
            if center_x_end <= center_x_start or center_y_end <= center_y_start:
                button_samples.append((0, 0, 0))
                continue
            
            cell_center = buttons_img[center_y_start:center_y_end, center_x_start:center_x_end]
            
            if cell_center.size == 0:
                button_samples.append((0, 0, 0))
                continue
            
            avg_color = cv2.mean(cell_center)[:3]
            color_rgb = (int(avg_color[2]), int(avg_color[1]), int(avg_color[0]))
            
            button_samples.append(color_rgb)
        
        return button_samples
    
    def visualize_detection_complete(self, img: np.ndarray, board: List[List[int]], board_region: tuple, 
                                     button_colors: List[int], buttons_region: tuple, grid_size: int):
        """Dibuja tablero y botones en una ÚNICA visualización"""
        debug_img = img.copy()
        
        colors_bgr = []
        for color_id in range(6):
            if color_id in self.color_calibration:
                r, g, b = self.color_calibration[color_id]
                colors_bgr.append((b, g, r))
            else:
                colors_bgr.append((100, 100, 100))
        
        # ===== DIBUJAR TABLERO =====
        x1, y1, x2, y2 = board_region
        board_width = x2 - x1
        board_height = y2 - y1
        
        cv2.rectangle(debug_img, (x1, y1), (x2-1, y2-1), (0, 0, 255), 3)
        
        for row in range(1, grid_size):
            y = y1 + int(row * board_height / grid_size)
            cv2.line(debug_img, (x1, y), (x2, y), (100, 100, 100), 1)
        
        for col in range(1, grid_size):
            x = x1 + int(col * board_width / grid_size)
            cv2.line(debug_img, (x, y1), (x, y2), (100, 100, 100), 1)
        
        for row in range(grid_size):
            y_start = int(row * board_height / grid_size)
            y_end = int((row + 1) * board_height / grid_size)
            cy = y1 + y_start + (y_end - y_start) // 2
            
            for col in range(grid_size):
                x_start = int(col * board_width / grid_size)
                x_end = int((col + 1) * board_width / grid_size)
                cx = x1 + x_start + (x_end - x_start) // 2
                
                color_id = board[row][col]
                color = colors_bgr[color_id]
                
                cv2.circle(debug_img, (cx, cy), 10, color, -1)
                cv2.circle(debug_img, (cx, cy), 10, (0, 0, 0), 1)
                cv2.putText(debug_img, str(color_id), (cx - 5, cy + 5),
                           cv2.FONT_HERSHEY_SIMPLEX, 0.4, (255, 255, 255), 1)
        
        # ===== DIBUJAR BOTONES =====
        bx1, by1, bx2, by2 = buttons_region
        button_width = bx2 - bx1
        button_height = by2 - by1
        num_buttons = 6
        
        cv2.rectangle(debug_img, (bx1, by1), (bx2-1, by2-1), (255, 0, 0), 3)
        
        for btn in range(1, num_buttons):
            x = bx1 + int(btn * button_width / num_buttons)
            cv2.line(debug_img, (x, by1), (x, by2), (150, 150, 150), 2)
        
        for btn in range(num_buttons):
            x_start = int(btn * button_width / num_buttons)
            x_end = int((btn + 1) * button_width / num_buttons)
            cx = bx1 + x_start + (x_end - x_start) // 2
            cy = by1 + button_height // 2
            
            color_id = button_colors[btn]
            color = colors_bgr[color_id]
            
            cv2.circle(debug_img, (cx, cy), 15, color, -1)
            cv2.circle(debug_img, (cx, cy), 15, (0, 0, 0), 2)
            cv2.putText(debug_img, str(color_id), (cx - 8, cy + 8),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)
        
        debug_bgr = cv2.cvtColor(debug_img, cv2.COLOR_RGB2BGR)
        
        output_path = "debug_detection.png"
        cv2.imwrite(output_path, debug_bgr)
        print(f"[+] Detección guardada en: {output_path}")
        
        cv2.imshow("Hamilton Flood - Tablero + Botones", debug_bgr)
        print("[*] Presiona cualquier tecla para continuar...")
        cv2.waitKey(0)
        cv2.destroyAllWindows()


class AutoClicker:
    
    
    def __init__(self):
        self.detector = GameDetector()
        self.delay = 1.0
    
    def run(self, grid_size: int = 18):
        
        print("\n Capturando...")
        time.sleep(1)
        screen = self.detector.capture_screen()
        
        print(" marca las regiones...")
        board_region, buttons_region = self.detector.mark_regions(screen)
        
        print("\n Detectando colores de botones...")
        button_samples = self.detector._get_button_samples(screen, buttons_region)
        button_colors = self.detector.detect_buttons_colors(screen, buttons_region)
        
        print(f"[+] Colores de botones detectados:")
        names = ["Rojo", "Azul", "Verde", "Amarillo", "Naranja", "Morado"]
        for i, color_id in enumerate(button_colors):
            print(f"    Botón {i}: RGB{button_samples[i]} -> Color {color_id} ({names[color_id]})")
        
        print(" Actualizando calibración...")
        for color_id in range(6):
            for btn_idx, detected_color_id in enumerate(button_colors):
                if detected_color_id == color_id:
                    self.detector.color_calibration[color_id] = button_samples[btn_idx]
                    break
        self.detector._save_calibration()
        
        print("[*] Detectando colores del tablero...")
        board = self.detector.detect_board_colors(screen, board_region, grid_size)
        
        if board is None:
            print("[-] Error en detección")
            return
        
        print("[*] Mostrando detección...")
        self.detector.visualize_detection_complete(screen, board, board_region, button_colors, buttons_region, grid_size)
        
        self._show_board(board)
        
        print("\n[*] Detectando ubicación de botones...")
        button_positions = self.detector.find_color_buttons_in_region(screen, buttons_region)
        
        buttons = {}
        for pos_idx in range(6):
            color_id = button_colors[pos_idx]
            if pos_idx in button_positions:
                buttons[color_id] = button_positions[pos_idx]
        
        if len(buttons) < 6:
            print(f"[-] Solo se encontraron {len(buttons)} botones, se necesitan 6")
            return
        
        print(f"[+] Botones en pantalla:")
        for color_id in sorted(buttons.keys()):
            x, y = buttons[color_id]
            print(f"    Color {color_id} ({names[color_id]}): ({x}, {y})")
        
        # Preguntar cantidad de intentos
        iterations = 31
        try:
            user_iterations = input(f"\n[?] ¿Cuántos intentos de solución? (default 31): ").strip()
            if user_iterations:
                iterations = int(user_iterations)
                if iterations <= 0:
                    print("[-] Número inválido, usando 31")
                    iterations = 31
        except ValueError:
            print("[-] Número inválido, usando 31")
            iterations = 31
        
        # Resolver con búsqueda inteligente
        print(f"\n[*] Resolviendo (máximo {iterations} movimientos)...")
        try:
            from openflood_solver import OpenFloodBoard, OpenFloodSolver
            game_board = OpenFloodBoard(grid_size, grid_size, 6, board=board)
            solver = OpenFloodSolver(game_board)
            
            # Usar solve_iddfs que usa Greedy + IDDFS internamente
            print(f"  Buscando solución ≤{iterations} movimientos (máximo 240 segundos)...")
            solution = solver.solve_iddfs(max_time=240.0)
            
            # Si falla el método híbrido, fallback a Greedy puro
            if not solution:
                print("  [-] Búsqueda híbrida sin resultado, intentando Greedy puro...")
                solution = solver.solve_greedy(iterations=iterations)
            
            if not solution:
                print("[-] No se encontró solución")
                return
            
            # Validar que no exceda el límite especificado
            if len(solution) > iterations:
                print(f"[-] Solución rechazada: {len(solution)} > {iterations} movimientos")
                print(f"    Se necesita encontrar una solución ≤{iterations}")
                return
            
            print(f"[+] Solución: {len(solution)} movimientos (≤{iterations}) ✓")
            print(f"    {' → '.join(map(str, solution))}")
        
        except Exception as e:
            print(f"[-] Error: {e}")
            return
        
        
        print("\n" + "="*60)
        input("\n  Presiona ENTER para CONFIRMAR y ejecutar... ")
    
        
        self._execute(solution, buttons)
    
    def _execute(self, solution: List, buttons: Dict):
        """Hace los clics"""
        for i, color in enumerate(solution, 1):
            if color not in buttons:
                print(f"[-] Color {color} no encontrado")
                return
            
            x, y = buttons[color]
            print(f"[{i}/{len(solution)}] Color {color} en ({x}, {y})")
            pyautogui.click(x, y)
            time.sleep(self.delay)
        
        print("\n[+] ¡Completado!")
    
    def _show_board(self, board: List[List[int]]):
        """Muestra el tablero"""
        emoji = ['🔴', '🔵', '🟢', '🟡', '🟠', '🟣']
        print("=" * 50)
        for row in board:
            print(" ".join(emoji[c] for c in row))
        print("=" * 50)


def main():
    
    while True:
        try:
            size = input("\nTamaño tablero (18 por defecto): ").strip()
            grid = int(size) if size else 18
            if grid > 0:
                break
        except:
            pass
    
    print("\n[!] Asegúrate que BlueStacks está visible")
    input("Presiona ENTER...")
    
    clicker = AutoClicker()
    clicker.run(grid)


if __name__ == "__main__":
    main()
