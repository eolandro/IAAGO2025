from pynput import mouse, keyboard

T = 6
B = {}

print("===============================================================")
print("                   CALIBRACION DE CURSOR                       ")
print("===============================================================")
print("Coloca el cursor donde quieres y presiona ESPACIO para guardar ")
print("===============================================================")
print("                Presiona ESC para cancelar.")
print("===============================================================")

P = None

def on_click(X, Y, button, pressed):
    global P
    if pressed:
        P = (X, Y)

def on_press(K):
    global I, P
    
    if K == keyboard.Key.esc:
        print("\nCalibración cancelada.")
        return False
    
    if K == keyboard.Key.space:
        if P is not None:
            B[I] = P
            print(f"Guardado {I}: {P}")
            I += 1
            
            if I > T:
                print("\n=== Calibración completa ===")
                print("\nCopia este diccionario en tu código:\n")
                print("B = {")
                for Kc, V in B.items():
                    print(f"    {Kc}: {V},")
                print("}")
                return False
        else:
            print("No se detectó posición del cursor aún.")

with mouse.Listener(on_click=on_click) as Ml:
    with keyboard.Listener(on_press=on_press) as Kl:
        I = 1
        Kl.join()
