import random
from ruamel.yaml import YAML

yaml = YAML()
with open('tablero.yaml', 'r') as file:
    data = yaml.load(file)
    matriz = data["tablero"]

columnas = "ABCDE"
casillas = {}

for i, fila in enumerate(matriz, start=1):
    for j, valor in enumerate(fila):
        clave = f"{columnas[j]}{i}"
        casillas[clave] = valor

def detector(valor):
    vacias10 = [0, 0, 0, 0, 0, 0, 0, 0, 1, 1]
    bombas10 = [1, 1, 1, 1, 1, 1, 1, 1, 1, 0]

    def custom_choice(lst):
        shuffled_list = lst[:]
        random.shuffle(shuffled_list)
        return shuffled_list[0]

    if valor == 1:
        return custom_choice(bombas10)
    else:
        return custom_choice(vacias10)

# Probabilidades
PPB = 9 / 10
PPBB = 1 / 10
PNBB = 2 / 10
PNNB = 8 / 10

dec = len(casillas)
cont = 0
des = 3
columnas = "ABCDE"

# RECORRIDO
for i in range(1, 11):
    if i % 2 == 0:
        letras = columnas
    else:
        letras = reversed(columnas)

    for letra in letras:
        clave = f"{letra}{i}"
        valor = casillas[clave]
        R = detector(valor)
        print(f"Valor de detector 1: {R}")
        if R == 1:
            PB = 1 / dec
            print(f"P(Bomba): {PB}")
            PNB = 1 - PB
            print(f"P(!Bomba): {PNB}")
            PBD = (PPB * PB) / ((PB * PPB) + (PNB * PNBB))
            print(f"P(Bomba|D+): {PBD}")
            PB = PBD
            while cont != 2:
                T = detector(valor)
                print(f"Valor de detector {cont + 2}: {T}")
                if T == 1:
                    print(f"P(Bomba) {cont + 1}: {PB}")
                    PNB = 1 - PB
                    print(f"P(!Bomba) {cont + 1}: {PNB}")
                    PBD = (PPB * PB) / ((PB * PPB) + (PNB * PNBB))
                    print(f"P(Bomba|D+ ) {cont + 1}: {PBD}")
                    PB = PBD
                cont += 1
            cont = 0
            if PBD >= 0.50:
                if des > 0:
                    des -= 1
                    print("\n°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°")
                    print(f"Bomba desactivada en: {clave}")
                    print("°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°\n")
            else:
                print(f"{clave}: {valor}")
        else:
            print(f"{clave}: {valor}")
        dec -= 1
        if des <= 0:
            print("Desactivadores agotados")
            break
    if des <= 0:
        break
