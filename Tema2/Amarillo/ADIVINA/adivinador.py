import json
from tabulate import tabulate
from unidecode import unidecode
import random

# Cargar el archivo JSON
with open("tabla_pesos.json", encoding='utf-8') as entrada:
    Datos = json.load(entrada)
print("\n///////////////////////////// A D I V I N A D O R //////////////////////////\n")
# Función para corregir texto con caracteres corruptos
def corregir_texto(texto):
    texto = unidecode(texto)  # Convertir caracteres especiales a ASCII
    # Reemplazar caracteres corruptos específicos
    texto = texto.replace('A+-', 'ñ').replace('A!', 'á').replace('A3n', 'ón')
    return texto

# Corregir el encabezado
encabezado = [corregir_texto(col) for col in Datos["encabezado"]]

# Convertir las filas en una lista de tuplas (o diccionarios) para facilitar la ordenación
filas_convertidas = []
for fila in Datos["filas"]:
    fila_corregida = {
        "nombre": corregir_texto(fila["nombre"]),
        "caracteristicas": {corregir_texto(k): v for k, v in fila["caracteristicas"].items()},
        "Total": fila["Total"]
    }
    # Convertir el valor binario a entero
    fila_corregida["Total_valor"] = int(fila["Total"], 2)
    filas_convertidas.append(fila_corregida)

# Ordenar las filas por el valor entero de "Total" en orden descendente
filas_ordenadas = sorted(filas_convertidas, key=lambda x: x["Total_valor"], reverse=True)

# Crear una lista de filas para la tabla
tabla = []
for fila in filas_ordenadas:
    fila_tabla = [fila["nombre"]]
    for carac in encabezado[1:-1]:  # Excluir "Animal" y "Total"
        fila_tabla.append(fila["caracteristicas"].get(carac, 0))  # Obtener cada característica o 0 si no existe
    fila_tabla.append(fila["Total"])
    tabla.append(fila_tabla)
    # Mostrar la tabla
print(tabulate(tabla, headers=encabezado, tablefmt="grid"))

print("Escoge un animal")

matriz = [encabezado] + tabla

c = 1  # Por ejemplo, buscamos el valor 1 en la columna "Acuático"
g = False
# Ciclo while que recorre las columnas según el valor de 'c'
while c < len(encabezado) - 1:
    if len(matriz) == 2:
        print(f"\n********* El animal que escogiste es {matriz[1][0]} ********************\n")
        break
    while True:
        R = input(f"¿El animal que escogiste tiene {encabezado[c]}? (s/n) => ").lower()
        if R in ['s', 'n']:
            break
        else:
            print("\nError: Debes ingresar 's' para sí o 'n' para no. Intenta de nuevo.\n")

    if R == 's':
        h = c + 1

        fila_c = [fila for fila in matriz[1:] if fila[c] == 1]
        num_columnas = len(fila_c[0])
        fila_d = fila_c

        for col in range(h, num_columnas):

            if len(fila_d) == 1:
                print(f"\n********* El animal que escogiste es {fila_d[0][0]} ********************\n")
                g = True
                break


            columna = [fila[col] for fila in fila_d]
            if len(set(columna)) != 1:

                while True:
                    t = input(f"¿El animal que escogiste tiene {encabezado[col]}? (s/n) => ").lower()
                    if t in ['s', 'n']:
                        break
                    else:
                        print("\nError: Debes ingresar 's' para sí o 'n' para no. Intenta de nuevo.\n")
                if t == 's':
                    fila_d = [fila for fila in fila_d if fila[col] != 0]

                    if len(fila_d) == 1 :
                        print(f"\n********* El animal que escogiste es {fila_d[0][0]} ********************\n")
                        g = True
                        break
                else:
                    fila_d = [fila for fila in fila_d if fila[col] != 1]

            if len(fila_d) == 2 and col == num_columnas - 1:
                j = random.randint(0, len(fila_d) - 1)
                while True:
                    e = input(f"¿El animal que escogiste tiene {fila_d[j][0]}? (s/n) => ").lower()
                    if e in ['s', 'n']:
                        break
                    else:
                        print("\nError: Debes ingresar 's' para sí o 'n' para no. Intenta de nuevo.\n")
                if e == 's':
                    g = True
                    break
                else:
                    for fila in fila_d:
                        if fila != fila_d[j]:
                            print(f"\n********* El animal que escogiste es {fila[0]} ********************\n")
                            g = True
                            break

    else:
        matriz = [fila for fila in matriz if fila[c] != 1]
        
    if g:
        break
    #print(fila_c)
    c = c + 1




