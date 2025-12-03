import numpy as np
import os
from ruamel.yaml import YAML

yaml = YAML()
yaml.indent(mapping=2, sequence=4, offset=2)

def CC(): 
    try:
        R = os.path.join("calibraciones", "calibrarB.yaml")
        
        if not os.path.exists(R):
            raise FileNotFoundError(f"No se encontró el archivo {R}")
        
        with open(R, "r") as f:
            datos = yaml.load(f) 
        
        if datos is None:
            raise ValueError("El archivo YAML está vacío")
        
        if 'botones' not in datos:
            raise KeyError("No se encontró la sección (botones)")
        
        BC = {} 
        BD = datos['botones'] 
        
        for key, value in BD.items():
            try:
                num = int(key.split('_')[1])
                BC[num] = tuple(value)
            except (ValueError, IndexError, KeyError) as e:
                print(f"Error al procesar {key}: {e}")
                continue
        
        if not BC:
            raise ValueError("No se cargaron las calibraciones")
        return BC
            
    except Exception as e:
        print(f"Error al cargar calibraciones")
        print("\nPor favor, ejecuta primero calibrarB.py")
        exit(1)

B = CC()

C = {
    1: {"n": "Rojo", "b": np.array([63, 57, 229])},
    2: {"n": "Azul", "b": np.array([253, 139, 112])},
    3: {"n": "Verde", "b": np.array([52, 156, 52])},
    4: {"n": "Amarillo", "b": np.array([45, 206, 255])},
    5: {"n": "Naranja", "b": np.array([66, 111, 254])},
    6: {"n": "Morado", "b": np.array([176, 60, 161])}
}

F, A, X, Y, W, H = 18, 18, 15, 189, 277, 277
