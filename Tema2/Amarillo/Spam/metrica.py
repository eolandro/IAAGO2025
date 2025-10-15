from ruamel.yaml import YAML

yaml = YAML()
Datos = False
resul = []
with open("msjetq2.yaml", 'r', encoding='utf-8') as entrada:
    Datos = yaml.load(entrada)

for i, msj in enumerate(Datos['mensajes']):
    if isinstance(msj, dict):
        mensaje_texto = list(msj.keys())[0]
    else:
        mensaje_texto = msj
 
    # Mostrar solo el mensaje
    R = input(f'¿El Mensaje: "{mensaje_texto}" es Spam? (s/n) => ')
    if R.lower() == 's':
        resul.append({mensaje_texto: True})
    else:
        resul.append({mensaje_texto: False})

# Ahora `resul` contiene la lista actualizada con los valores de True o False para cada mensaje
print("\n" + "=" * 30)
print("     Supervisor    ")
print("=" * 30,"\n")

for item in resul:
    mensaje, es_spam = list(item.items())[0]
    clasificacion = 'SPAM' if es_spam else 'NO SPAM'
    print(f'Mensaje: "{mensaje}" - Clasificación: {clasificacion}')

print("\n" + "=" * 30)
print("     Clasificador    ")
print("=" * 30,"\n")


for msj in Datos['mensajes']:
    if isinstance(msj, dict):
        mensaje_texto, valor = list(msj.items())[0]
        clasificacion = "SPAM" if valor else "NO SPAM"
        print(f'Mensaje: "{mensaje_texto}" - Clasificación: {clasificacion}')

coincidencias = 0

# Comparar los resultados del supervisor con los datos originales
for i, msj in enumerate(Datos['mensajes']):
    if isinstance(msj, dict):
        mensaje_texto, valor_original = list(msj.items())[0]  # Valor original en Datos
    else:
        mensaje_texto = msj
        valor_original = False  # Si no es un dict, asumimos que el valor original es False

    valor_resul = resul[i][mensaje_texto]  # Valor clasificado por el supervisor

    # Verificar si ambos coinciden
    if valor_resul == valor_original:
        coincidencias += 1

# Mostrar el resultado de la comparación
print("\n" + "=" * 30)
print(" Comparación de resultados ")
print("=" * 30,"\n")
print(f'El número de coincidencias es: {coincidencias}')
print(f'Total de mensajes comparados: {len(Datos["mensajes"])}')

# --- Calcular métricas de rendimiento ---

TP = FP = FN = TN = 0

for i, msj in enumerate(Datos['mensajes']):
    if isinstance(msj, dict):
        mensaje_texto, valor_original = list(msj.items())[0]
    else:
        mensaje_texto = msj
        valor_original = False  # si no está marcado, asumimos no spam

    valor_resul = resul[i][mensaje_texto]

    if valor_original and valor_resul:
        TP += 1
    elif not valor_original and valor_resul:
        FP += 1
    elif valor_original and not valor_resul:
        FN += 1
    else:
        TN += 1

total = TP + FP + FN + TN
accuracy = (TP + TN) / total if total != 0 else 0
precision = TP / (TP + FP) if (TP + FP) != 0 else 0
recall = TP / (TP + FN) if (TP + FN) != 0 else 0
f1 = 2 * (precision * recall) / (precision + recall) if (precision + recall) != 0 else 0
prevalencia = (TP + FN) / total if total != 0 else 0

print("\n" + "=" * 30)
print("   MÉTRICAS DE RENDIMIENTO")
print("=" * 30)
print(f"TP (Spam bien detectado): {TP}")
print(f"FP (Falsos positivos): {FP}")
print(f"FN (Falsos negativos): {FN}")
print(f"TN (No spam bien detectado): {TN}")
print(f"\nAccuracy: {accuracy:.2f}")
print(f"Precisión: {precision:.2f}")
print(f"Recall: {recall:.2f}")
print(f"F1-Score: {f1:.2f}")
print(f"Prevalencia: {prevalencia:.2f}")
