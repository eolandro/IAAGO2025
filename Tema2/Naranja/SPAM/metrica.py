import yaml

with open("respuestas2.yaml", "r", encoding="utf-8") as f:
    resultados_modelo = yaml.safe_load(f)

print("\n======== EVALUACIÓN DEL CLASIFICADOR ========\n")

supervisor = {}

for mid, info in resultados_modelo.items():
    texto = info["texto"]
    clas_modelo = info["clasificacion"]
    
    while True:
        resp = input(f"MENSAJE: {texto}\n¿Es SPAM realmente? (s/n): ").strip().lower()
        if resp in ("s", "n"):
            supervisor[mid] = (resp == "s")
            print()
            break
        else:
            print("Ingresa solo 's' si es spam o 'n' si no lo es.\n")

# Comparar resultados
VP = FP = VN = FN = 0  

for mid, info in resultados_modelo.items():
    pred_spam = (info["clasificacion"] == "spam")
    real_spam = supervisor[mid]

    if pred_spam and real_spam:
        VP += 1
    elif pred_spam and not real_spam:
        FP += 1
    elif not pred_spam and not real_spam:
        VN += 1
    elif not pred_spam and real_spam:
        FN += 1

total = VP + FP + VN + FN

# Calculo de metricas
def safe_div(num, den):
    return round(num / den, 3) if den != 0 else 0.0

recall = safe_div(VP, VP + FN)
accuracy = safe_div(VP + VN, total)
precision = safe_div(VP, VP + FP)
prevalence = safe_div(VP + FN, total)

# Guardar resultados
metricas = {
    "Verdaderos_Positivos (VP)": VP,
    "Falsos_Positivos (FP)": FP,
    "Verdaderos_Negativos (VN)": VN,
    "Falsos_Negativos (FN)": FN,
    "Total_mensajes": total,
    "Recall": recall,
    "Accuracy": accuracy,
    "Precision": precision,
    "Prevalence": prevalence
}

with open("resultado_metricas.yaml", "w", encoding="utf-8") as f:
    yaml.dump(metricas, f, allow_unicode=True)


print("\n============ RESULTADOS DE LA EVALUACIÓN ============")
print(f"Verdaderos Positivos (VP): {VP} → Mensajes que eran spam y el modelo los detectó correctamente.")
print(f"Falsos Positivos (FP): {FP} → Mensajes que no eran spam pero el modelo los marcó como spam.")
print(f"Verdaderos Negativos (VN): {VN} → Mensajes normales que el modelo dejó pasar correctamente.")
print(f"Falsos Negativos (FN): {FN} → Mensajes que sí eran spam pero el modelo no los detectó.\n")

print(f"Accuracy: {accuracy}  → Porcentaje total de aciertos.")
print(f"Recall: {recall}  → Capacidad para detectar spam real.")
print(f"Precision: {precision}  → Mensajes marcados como spam que realmente lo eran.")
print(f"Prevalence: {prevalence}  → Proporción real de spam en los mensajes evaluados.\n")
