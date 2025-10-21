from pathlib import Path
import sys
import json


def cargar_datos_figura(archivo='figuras.json'):
    ruta = Path('.') / archivo
    try:
        with ruta.open(encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"No existe el archivo {archivo}")
        sys.exit(1)
    except (json.JSONDecodeError, UnicodeDecodeError) as e:
        print(f"Error al cargar el archivo JSON: {e}")
        sys.exit(1)


def obtener_respuesta_usuario(pregunta, opciones=None, es_si_no=False):
    print(f"\n{pregunta}")
    opciones = {0, 1} if es_si_no else set(opciones or [])
    print("Ingrese 1 para 'Sí' o 0 para 'No'" if es_si_no else "Opciones: " + ' '.join(map(str, opciones)))
    
    while True:
        try:
            respuesta = int(input("> "))
            (respuesta in opciones) or (_ for _ in ()).throw(ValueError)
            return respuesta
        except ValueError:
            print("Valor inválido, inténtelo de nuevo.")


def es_estado_final(estado, preguntas):
    return estado not in preguntas


def obtener_siguiente_estado(estado_actual, respuesta, transiciones):
    return next((t[2] for t in transiciones if t[0] == estado_actual and t[1] == respuesta), None)


def main():
    datos = cargar_datos_figura()
    estado = datos['EstadoInicial']
    estados = {e[0]: e for e in datos['Estados']}
    
    print("=" * 50)
    print("ADIVINANDO LAS FIGURAS GEOMÉTRICAS")
    print("=" * 50)
    print("\nEMPEZAMOS :)\n")

    try:
        while True:
            actual = estados.get(estado)
            
            if es_estado_final(estado, datos['Preguntas']): 
                print("\n" + "=" * 40)
                print(f"¡TU FIGURA ES!: {actual[1]}")
                print("=" * 40)
                break
            
            pregunta = datos['Preguntas'][estado]
            respuesta = obtener_respuesta_usuario(pregunta, actual[1:], len(actual) == 3)
            siguiente = obtener_siguiente_estado(estado, respuesta, datos['Transiciones'])
            
            (siguiente is not None) or (_ for _ in ()).throw(Exception("No se encontró transición válida")) 
            estado = siguiente

    except KeyboardInterrupt:
        print("\n\nPrograma interrumpido por el usuario")
    except Exception as e:
        print(f"\nError inesperado: {e}")


if __name__ == "__main__":
    main()
