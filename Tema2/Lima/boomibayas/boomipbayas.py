import yaml
import random

P_DETECTAR_SI_BOMBA = 0.9
P_DETECTAR_SI_VACIO = 0.2

def cargar_mapa(ruta):
    with open(ruta, "r") as f:
        datos = yaml.safe_load(f)
    return datos["mapa"]

def obtener_posicion_bomba(mapa):
    for i, fila in enumerate(mapa):
        for j, valor in enumerate(fila):
            if valor == 1:
                return i, j
    return None, None

def probabilidad_bayesiana(P_B, detectado):
    if detectado:
        numerador = P_DETECTAR_SI_BOMBA * P_B
        denominador = (P_DETECTAR_SI_BOMBA * P_B) + (P_DETECTAR_SI_VACIO * (1 - P_B))
    else:
        P_no_detectar_si_bomba = 1 - P_DETECTAR_SI_BOMBA
        P_no_detectar_si_vacio = 1 - P_DETECTAR_SI_VACIO
        numerador = P_no_detectar_si_bomba * P_B
        denominador = (P_no_detectar_si_bomba * P_B) + (P_no_detectar_si_vacio * (1 - P_B))
    return numerador / denominador

def buscar_bomba(mapa):
    filas = len(mapa)
    columnas = len(mapa[0])
    bomba_fila, bomba_col = obtener_posicion_bomba(mapa)

    N = filas * columnas
    P_B = 1 / N  

    for fila in range(filas):
        if fila % 2 == 0:
            rango = range(columnas)
        else:
            rango = reversed(range(columnas))

        for col in rango:
            print(f"\nRevisando casilla ({fila}, {col})...")
            hay_bomba = (fila == bomba_fila and col == bomba_col)

            detectado = random.random() < (P_DETECTAR_SI_BOMBA if hay_bomba else P_DETECTAR_SI_VACIO)
            P_actual = probabilidad_bayesiana(P_B, detectado)
            print(f"Probabilidad calculada de bomba en esta casilla: {P_actual:.4f}")

            if detectado:
                positivos = 1
                P_total = P_actual  

                for intento in range(2):
                    confirmacion = (P_DETECTAR_SI_BOMBA if hay_bomba else P_DETECTAR_SI_VACIO)
                    print(f"  → Revisión {intento+2}: {'Positivo' if confirmacion else 'Negativo'}")

                    P_total = probabilidad_bayesiana(P_total, confirmacion)
                    print(f"    Probabilidad actualizada: {P_total:.4f}")

                    if P_total >= 0.5:
                        if hay_bomba:
                            print(f"\n¡Boomie confirmó la bomba en ({fila}, {col}) con {P_total*100:.2f}% de certeza!")
                            return True
                        else:
                            print(f"Falsa alarma: alta probabilidad ({P_total*100:.2f}%) pero sin bomba real.")
                            break

                if P_total < 0.5:
                    print(f"Probabilidad final ({P_total*100:.2f}%) insuficiente, Boomie sigue buscando...")
                elif hay_bomba:
                    print(f"\n¡Boomie encontró la bomba en ({fila}, {col}) tras 3 revisiones!")
                    return True

            N = N - 1
            print(f"Casillas restantes: {N}")
            P_B = 1 / N if N > 0 else 0

    print("\nBoomie falló y explotó... no encontró la bomba.")
    return False

if __name__ == "__main__":
    mapa = cargar_mapa("mapa.yaml")
    buscar_bomba(mapa)
