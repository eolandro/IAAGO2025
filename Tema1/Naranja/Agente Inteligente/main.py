import argparse
import AnalizadorLS as ALS
import BVM
from pathlib import Path

parser = argparse.ArgumentParser()
parser.add_argument("Archivo", help="Codigo de boomie", type=Path)

args = parser.parse_args()
if args.Archivo.exists():
    with args.Archivo.open() as codigo_fuente:
        vm = BVM.BVM()
        
        # Leer todas las líneas del archivo
        lineas = codigo_fuente.readlines()
        
        # Validar sintácticamente todo el programa primero
        programa_valido = True
        for i, linea in enumerate(lineas):
            linea_limpia = linea.strip()
            if not linea_limpia:
                continue
                
            L = [l for l in linea_limpia.split(' ') if l]
            resultado = ALS.linea_codigo(L)
            
            if not resultado[0]:
                print(f"✗ ERROR SINTÁCTICO en línea {i+1}: {linea_limpia}")
                print(f"  Razón: {resultado[1]}")
                programa_valido = False
                break
        
        # Si el programa es válido, ejecutarlo
        if programa_valido:
            vm.cargar_programa(lineas)
            vm.ejecutar()
        else:
            print("Programa contiene errores. No se puede ejecutar.")