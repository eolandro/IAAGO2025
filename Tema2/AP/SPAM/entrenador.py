from ruamel.yaml import YAML
import sys

def entrenador():
    yaml = YAML()
    mensajes_etiquetados = {}
    
    try:
        with open('msg.yaml', 'r', encoding='utf-8') as f:
            mensajes = yaml.load(f)
    except FileNotFoundError:
        print("Archivo no encontrado")
        return

    if mensajes:
        for id_msg, contenido_msg in mensajes.items():
            
            while True:
                print(f"\nMensaje: {id_msg}")
                print(contenido_msg)
                respuesta = input("Clasificar como SPAM? (si/no): ").lower().strip()
                
                if respuesta in ['si', 'no']:
                    etiqueta = 'SPAM' if respuesta == 'si' else 'NO_SPAM'
                    mensajes_etiquetados[id_msg] = {
                        'mensaje': contenido_msg,
                        'etiqueta': etiqueta
                    }
                    break
                else:
                    print("respuesta invalida")
                    
        nombre_archivo_salida = 'msg_eti.yaml'
        
        try:
            with open(nombre_archivo_salida, 'w', encoding='utf-8') as f:
                yaml.dump(mensajes_etiquetados, f)

            print(f"Archivo '{nombre_archivo_salida}' creado")

            
        except Exception as e:
            print(f"error {e}")
        
    return mensajes_etiquetados

entrenador()
