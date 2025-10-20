from ruamel.yaml import YAML
import sys

def calcular_metricas_interactivo():
    yaml = YAML()
    
    try:
        with open('etiqueta2.yaml', 'r', encoding='utf-8') as f:
            predicciones = yaml.load(f)
        
    except FileNotFoundError:
        print("no esta etiqueta2.yaml")
        return None
    etiquetas_reales = {}
    
    for id_msg, data in predicciones.items():
        contenido_msg = data['mensaje']
        
        while True:
            print(f"Mensaje: {id_msg}")
            print(contenido_msg)
            respuesta = input("Clasificacion REAL (si=SPAM / no=NO_SPAM): ").lower().strip()
            
            if respuesta in ['si', 'no']:
                etiqueta_real = 'SPAM' if respuesta == 'si' else 'NO_SPAM'
                etiquetas_reales[id_msg] = etiqueta_real
                print(f"Predicción del CLASIFICADOR: {data['etiqueta']}")
                break
            else:
                print("escriba 'si' o 'no'.")
                

    
    vp, fp, fn, vn = 0, 0, 0, 0
    n_total = len(predicciones)
    
    for id_msg, data in predicciones.items():
        etiqueta_predicha = data['etiqueta']
        etiqueta_real = etiquetas_reales.get(id_msg)
        
        if etiqueta_real == 'SPAM' and etiqueta_predicha == 'SPAM':
            vp += 1  # Verdadero Positivo
        elif etiqueta_real == 'NO_SPAM' and etiqueta_predicha == 'SPAM':
            fp += 1  # Falso Positivo
        elif etiqueta_real == 'SPAM' and etiqueta_predicha == 'NO_SPAM':
            fn += 1  # Falso Negativo
        elif etiqueta_real == 'NO_SPAM' and etiqueta_predicha == 'NO_SPAM':
            vn += 1  # Verdadero Negativo

    # Calculo_metricas
    n_spam_real = vp + fn
    
    accuracy = (vp + vn) / n_total if n_total else 0
    recall = vp / (vp + fn) if (vp + fn) else 0 
    precision = vp / (vp + fp) if (vp + fp) else 0 
    prevalence = n_spam_real / n_total if n_total else 0 


    print("RESULTADOS:")
    print(f"\nTotal de Mensajes Evaluados: {n_total}")
    print(f"\nMatriz de Confusion: VP={vp}, FP={fp}, FN={fn}, VN={vn}")
    print(f"Accuracy (Exactitud): {accuracy:.3f}")
    print(f"Recall (Sensibilidad): {recall:.3f}")
    print(f"Precision (Precision): {precision:.3f}")
    print(f"Prevalence (Prevalencia): {prevalence:.3f}")
    
    return {
        "Accuracy": accuracy, "Recall": recall, "Precision": precision, 
        "Prevalence": prevalence, "Matriz_Confusión": {"VP": vp, "FP": fp, "FN": fn, "VN": vn}
    }

calcular_metricas_interactivo()
