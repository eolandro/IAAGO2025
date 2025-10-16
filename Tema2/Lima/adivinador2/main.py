import argparse
#import AnaliLS as ALS
import Adivinador1 as ADV
import json
from pathlib import Path

parser = argparse.ArgumentParser()
parser.add_argument(
    "Archivo", help="Archivo: ", type=Path
)

args = parser.parse_args()
adv=ADV.Adivinador()
if args.Archivo.exists():
    print("Codigo Fuente encontrado")
    with args.Archivo.open('r') as arch_json:
        #for i in arch_yml:
            #datos= [a for a in arch_yml]
            #datos= yaml.safe_load(arch_yml)
            #ent.imprimir(datos)
        datos = json.load(arch_json)      # leer archivo JSON
        preguntas = datos.get("Preguntas", {})  # solo la parte de Preguntas
        parametros = datos["Transcisiones"]  # solo la parte de Parametros
        adv.datos(preguntas,parametros) 
        adv.preguntas()
            