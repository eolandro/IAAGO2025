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
		for linea in codigo_fuente:
			#print(linea.strip())
			L = [ l for l in linea.strip().split(' ') if l ]
			print(L)
			U = ALS.linea_codigo(L)
			if U:
				print(vm)
				vm.Instruccion = L 
				vm.ejecutarInstruccion()
				print(vm)
