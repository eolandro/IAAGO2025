import argparse
import AnaliLS as ALS
import BVM 
from pathlib import Path

parser = argparse.ArgumentParser()
parser.add_argument(
    "Archivo", help="Codigo de Boome: ", type=Path
)

args = parser.parse_args()

if args.Archivo.exists():
    print("Codigo Fuente encontrado")
    with args.Archivo.open() as codigo_fuente:
        lineas = [linea.strip() for linea in codigo_fuente]

    vm = BVM.BVM()

    while vm.PC < len(lineas) and vm.Estado != 'Morido':
        L = [l for l in lineas[vm.PC].split(" ") if l]
        print(L)

        pc_actual = vm.PC  
        U = ALS.linea_codigo(L)
        if U:
            print(vm)
            vm.Instruccion = L
            vm.ejecutarInstruccion()
            print(vm)

        if vm.PC == pc_actual:
            vm.PC += 1

