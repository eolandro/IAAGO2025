def mostrar_tablero(tablero):
    for i in range(5):
        espacios = ' ' * (4 - i)
        fila = []
        for j in range(i + 1):
            if tablero[i][j] == 1:
                fila.append('O')
            else:
                fila.append('x')
        print(espacios + ' '.join(fila))

def resolver_juego(fila_vacia, columna_vacia):
  
    tablero = []
    for i in range(5):
        fila = []
        for j in range(i + 1):
            if i == fila_vacia and j == columna_vacia:
                fila.append(0)  
            else:
                fila.append(1)  
        tablero.append(fila)
    
  
    cola = [(tablero, [])]  
    visitados = set()
    visitados.add(str(tablero))
    
    while cola:
        tab_actual, movimientos = cola.pop(0)
        
        
        fichas = 0
        for fila in tab_actual:
            fichas += sum(fila)
        
        if fichas == 1:
            return movimientos
        
    
        for i in range(5):
            for j in range(i + 1):
                if tab_actual[i][j] == 1: 
                    
                    for dx, dy in [(0,2), (0,-2), (2,0), (-2,0), (2,2), (-2,-2)]:
                        ni, nj = i + dx, j + dy  
                        mi, mj = i + dx//2, j + dy//2 
                        
                      
                        if (0 <= ni < 5 and 0 <= nj <= ni and
                            tab_actual[ni][nj] == 0 and tab_actual[mi][mj] == 1):
                            
                           
                            nuevo_tab = [fila[:] for fila in tab_actual]
                            nuevo_tab[i][j] = 0
                            nuevo_tab[ni][nj] = 1
                            nuevo_tab[mi][mj] = 0
                            
                          
                            if str(nuevo_tab) not in visitados:
                                nuevo_mov = movimientos + [(i, j, ni, nj)]
                                cola.append((nuevo_tab, nuevo_mov))
                                visitados.add(str(nuevo_tab))
    
    return None 

def main():
    print("-------- COME SOLO--------")
    print("\nTablero con coordenadas:")
    for i in range(5):
        espacios = ' ' * (4 - i)
        coordenadas = []
        for j in range(i + 1):
            coordenadas.append(f"{i},{j}")
        print(espacios + ' '.join(coordenadas))
    
    print("\nDonde quieres empezar:")
    fila = int(input("Fila: "))
    columna = int(input("Columna: "))
    
    print("\nSolucion.")
    solucion = resolver_juego(fila, columna)
    
    if solucion:
        print(f"\nSi se pudoo...en {len(solucion)}")
        
   
        tablero = []
        for i in range(5):
            fila_tab = []
            for j in range(i + 1):
                if i == fila and j == columna:
                    fila_tab.append(0)
                else:
                    fila_tab.append(1)
            tablero.append(fila_tab)
        
        print("\nEstado inicial:")
        mostrar_tablero(tablero)
        
        for paso, (x, y, nx, ny) in enumerate(solucion, 1):
           
            mx, my = (x + nx) // 2, (y + ny) // 2  #
            tablero[x][y] = 0
            tablero[nx][ny] = 1
            tablero[mx][my] = 0
            
            print(f"\nMovimiento {paso}: ({x},{y}) → ({nx},{ny})")
            mostrar_tablero(tablero)
    else:
        print("No se pudo encontra la soluicon")

if __name__ == "__main__":
    main()