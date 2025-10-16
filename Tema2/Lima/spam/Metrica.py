import yaml
import re

# === Archivos de entrada/salida ===
archivo_txt = "10msjspam2.txt"  # Contiene los mensajes con etiquetas reales
archivo_resultados = "clasificador2.yaml"  # Contiene las predicciones
archivo_metricas = "metricas_evaluacion2.yaml"  # Archivo de salida con métricas

# === 1. Leer etiquetas reales del TXT ===
with open(archivo_txt, "r", encoding="utf-8") as f:
    contenido = f.read()

# Extraer pares (etiqueta, mensaje)
patron = re.compile(r'(?i)^\s*(SPAM|NO\s*SPAM)\s*\n*\s*"(.+?)"', re.DOTALL | re.MULTILINE)
pares = patron.findall(contenido)

etiquetas_reales = {}
for etiqueta, mensaje in pares:
    mensaje_limpio = mensaje.strip().replace('\n', ' ')
    etiqueta_normalizada = "spam" if etiqueta.strip().upper() == "SPAM" else "no_spam"
    etiquetas_reales[mensaje_limpio] = etiqueta_normalizada

# === 2. Leer clasificaciones predichas ===
with open(archivo_resultados, "r", encoding="utf-8") as f:
    clasificaciones = yaml.safe_load(f)

# === 3. Emparejar mensajes y contar TP, FP, TN, FN ===
TP = FP = TN = FN = 0
comparaciones = []

for msg, real in etiquetas_reales.items():
    prediccion = None
    for m in clasificaciones:
        if m.strip().replace('\n', ' ') == msg:
            prediccion = clasificaciones[m]["clasificacion"]
            break

    if prediccion is None:
        comparaciones.append((msg, real, "NO_ENCONTRADO"))
        continue

    comparaciones.append((msg, real, prediccion))

    if real == "spam" and prediccion == "spam":
        TP += 1
    elif real == "no_spam" and prediccion == "spam":
        FP += 1
    elif real == "no_spam" and prediccion == "no_spam":
        TN += 1
    elif real == "spam" and prediccion == "no_spam":
        FN += 1

# === 4. Calcular métricas ===
total = TP + FP + TN + FN
accuracy = (TP + TN) / total if total else 0
precision = TP / (TP + FP) if (TP + FP) else 0
recall = TP / (TP + FN) if (TP + FN) else 0
specificity = TN / (TN + FP) if (TN + FP) else 0
prevalence = (TP + FN) / total if total else 0
f1 = 2 * (precision * recall) / (precision + recall) if (precision + recall) else 0

# === 5. Guardar métricas en YAML ===
metricas = {
    "Accuracy": round(accuracy, 3),
    "Precision": round(precision, 3),
    "Recall": round(recall, 3),
    "Specificity": round(specificity, 3),
    "Prevalence": round(prevalence, 3),
    "F1-score": round(f1, 3)
}

with open(archivo_metricas, "w", encoding="utf-8") as f:
    yaml.dump(metricas, f, allow_unicode=True, sort_keys=False)

print(f"Archivo '{archivo_metricas}' generado con las métricas de evaluación.\n")

# === 6. Mostrar comparaciones (opcional) ===
print("\n=== CLASIFICACIONES COMPARADAS ===")
for i, (msg, real, pred) in enumerate(comparaciones, start=1):
    print(f"\n[{i}] {msg[:80]}...")
    print(f"  → Real: {real} | Predicha: {pred}")
