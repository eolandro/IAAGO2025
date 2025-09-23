import argparse
from pathlib import Path
import BVM  
import AnalizadorLS as ALS

parser = argparse.ArgumentParser()
parser.add_argument(
	"Archivo", help="Codigo de boome", type= Path
)

args = parser.parse_args()
if args.Archivo.exists():
    print("Codigo fuente encontrado")
    with args.Archivo.open() as codigo_fuente:
        vm = BVM.BVM()
        
        codigo_lineas = [line.strip() for line in codigo_fuente if line.strip()]
        instrucciones_parseadas = []
        for i, linea_str in enumerate(codigo_lineas):
            LS = [l for l in linea_str.split(' ') if l]
            R_valida, V_valida = ALS.linea_codigo(LS)
            if not R_valida:
                print(f"Error de sintaxis en la línea {i+1}: {linea_str} -> {V_valida}")
                exit() 
            instrucciones_parseadas.append(LS)

        while vm.Estado == 'Activo' and vm.PC < len(instrucciones_parseadas):
            current_instruction_index = vm.PC
            current_instruction = instrucciones_parseadas[current_instruction_index]
            
            print(f"\n* * * * Ejecutando línea {current_instruction_index + 1}: {current_instruction} * * *")
            print(vm)
            
            vm.Instruccion = current_instruction
            vm.ejecutarInstruccion()
            
            print(vm) 
            if vm.PC == current_instruction_index: 
                vm.PC += 1
            
        if vm.Estado == 'Morido':
            print("\nLa El boome a (Estado: Morido)")
        else:
            print("\n * * * Fin * * * ")
