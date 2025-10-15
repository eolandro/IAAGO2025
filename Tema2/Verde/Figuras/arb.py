import json

class Nodo:
    def __init__(self, nombre, valor_arista=None, informacion=None):
        self.nombre = nombre 
        self.valor_arista = valor_arista  
        self.informacion = informacion  
        self.hijos = [] 

  
    def agregar_hijo(self, nodo_hijo, valor_arista):
        nodo_hijo.valor_arista = valor_arista
        self.hijos.append(nodo_hijo)


nodos = {}


def crear_arbol(transiciones, preguntas):
    
    for padre_id, arista, hijo_id in transiciones:

        nodo_padre = nodos.setdefault(padre_id, Nodo(nombre=padre_id))
        nodo_hijo = nodos.setdefault(hijo_id, Nodo(nombre=hijo_id))


        nodo_padre.agregar_hijo(nodo_hijo, arista)

    
    for nodo_id, info in preguntas.items():
        if nodo_id in nodos:
            nodos[nodo_id].informacion = info

def recorrido_dfs(nodo):

    if nodo.hijos:

        respuesta = input(f"\n {nodo.informacion} => ")
    else:
        
        print("\n********************************")
        print(f"Tu figura es: {nodo.informacion}")
        print("********************************")
        return 

   
    encontrado = False
    for hijo in nodo.hijos:
      
        if hijo.valor_arista.lower() == respuesta.lower():
            encontrado = True
            recorrido_dfs(hijo)  
            break
    
    if not encontrado:
        print("\nLo siento, esa respuesta no es válida. Por favor, intenta de nuevo.")
        recorrido_dfs(nodo) 



print("********************************")
print("      Adivinador de Figuras")
print("********************************")
print("\n¡Bienvenido! Responde a las preguntas para adivinar tu figura.")
print("Respuestas posibles: 'Si', 'No', o un número cuando se pida.\n")

try:
  
    with open("figuras.json", encoding='utf-8') as entrada:
        datos = json.load(entrada)

 
    transiciones = datos["Transiciones"]
    preguntas = datos["Preguntas"]
    
    crear_arbol(transiciones, preguntas)
    
    recorrido_dfs(nodos["A"])

except FileNotFoundError:
  
    print("Error: No se encontró 'hola.json'. Verifica que el archivo esté en la misma carpeta que el script y que el nombre sea exacto.")
except KeyError:
    print("Error: El archivo JSON no tiene las claves 'Transiciones' o 'Preguntas' requeridas.")
except Exception as e:
    print(f"Ocurrió un error inesperado: {e}")
