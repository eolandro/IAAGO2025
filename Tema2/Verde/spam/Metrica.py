from ruamel.yaml import YAML

yaml = YAML()

try:
    with open("mensajes_clasificados.yaml", 'r', encoding='utf-8') as entrada:
        datos_clasificador = yaml.load(entrada)
except FileNotFoundError:
    print("No se encontró 'mensajes_clasificados.yaml'")
    print("Por favor, ejecute 'clasificador.py' primero.")
    exit()

y_pred = []
mensajes_para_evaluar = []
for msj_dict in datos_clasificador['mensajes']:
    mensaje, es_spam_predicho = list(msj_dict.items())[0]
    y_pred.append(es_spam_predicho)
    mensajes_para_evaluar.append(mensaje)

print("--- EVALUACIÓN ---")
print("Clasifica los 10 mensajes  ")

y_true = []
for msj in mensajes_para_evaluar:
    respuesta = ""
    while respuesta not in ['s', 'n']:
        respuesta = input(f'\nMensaje: "{msj}"\n¿Es Spam? (s/n) => ')
    
    es_spam_real = True if respuesta.lower() == 's' else False
    y_true.append(es_spam_real)

TP = 0 
TN = 0
FP = 0 
FN = 0 

total_mensajes = len(y_true)

for i in range(total_mensajes):
    predicho = y_pred[i] 
    real = y_true[i]      

    if predicho == True and real == True:
        TP += 1
    elif predicho == False and real == False:
        TN += 1
    elif predicho == True and real == False:
        FP += 1
    elif predicho == False and real == True:
        FN += 1


print("      RESULTADOS DE EVALUACIÓN      ")


print("--- Matriz de Confusión ---")
print(f"               | Predicho: SPAM | Predicho: NO SPAM")
print(f"-----------------|----------------|-----------------")
print(f"Real: SPAM       |      {TP:^4}      |       {FN:^4}")
print(f"Real: NO SPAM    |      {FP:^4}      |       {TN:^4}")
print("\n")
print(f"TP (Verdadero Positivo): {TP} - (Dijo SPAM y SÍ era SPAM)")
print(f"TN (Verdadero Negativo): {TN} - (Dijo NO SPAM y NO era SPAM)")
print(f"FP (Falso Positivo):     {FP} - (Dijo SPAM pero NO era SPAM) <--- Error Tipo I")
print(f"FN (Falso Negativo):     {FN} - (Dijo NO SPAM pero SÍ era SPAM) <--- Error Tipo II")

print("\n--- Métricas Clave ---")

try:
    accuracy = (TP + TN) / total_mensajes
    print(f"1. Accuracy (Exactitud): {accuracy:.2%} de aciertos totales.")
except ZeroDivisionError:
    print("1. Accuracy (Exactitud): No se puede calcular (Total = 0)")

try:
    precision = TP / (TP + FP)
    print(f"2. Precision (Precisión): {precision:.2%} de los que dijo SPAM, acertó.")
except ZeroDivisionError:
    print("2. Precision (Precisión): No se puede calcular (No predijo ningún SPAM)")

try:
    recall = TP / (TP + FN)
    print(f"3. Recall (Sensibilidad): {recall:.2%} de todo el SPAM real, se encontró.")
except ZeroDivisionError:
    print("3. Recall (Sensibilidad): No se puede calcular (No había SPAM real)")

try:
    prevalence = (TP + FN) / total_mensajes
    print(f"4. Prevalence (Prevalencia): {prevalence:.2%} de los mensajes eran SPAM real.")
except ZeroDivisionError:
    print("4. Prevalence (Prevalencia): No se puede calcular (Total = 0)")

