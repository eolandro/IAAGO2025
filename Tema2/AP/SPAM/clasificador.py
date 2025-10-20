from ruamel.yaml import YAML
import numpy as np
import sys
from collections import defaultdict

def clasificador_por_consenso():
    yaml = YAML()
    try:
        with open('tabla_prob.yaml', 'r', encoding='utf-8') as f:
            tabla_prob = yaml.load(f)
        
    except FileNotFoundError:
        print("no se encontro la tabla de probabilidades")
        return None
    
    try:
        with open('msg2.yaml', 'r', encoding='utf-8') as f:
            mensajes_nuevos = yaml.load(f)
        
    except FileNotFoundError:
        print("falta msg2.yaml")
        return None

    clases = list(tabla_prob.keys()) 
    stop_words = set([
        'el', 'la', 'los', 'las', 'un', 'una', 'unos', 'unas', 'de', 'a', 'ante', 
        'bajo', 'con', 'contra', 'en', 'entre', 'hacia', 'hasta', 'para', 'por', 
        'según', 'sin', 'sobre', 'tras', 'y', 'o', 'del', 'al', 'tu', 'su', 'mi', 
        'te', 'que', 'es', 'ha', 'sus', 'sus', 'los', 'que', 'se', 'una', 'un', 
        'suya', 'mio', 'mía', 'mío', 'mi', 'usted', 'eso', 'esto', 'aquello', 'qué',
        'quién', 'como', 'donde', 'cuando', 'este', 'esta', 'estos', 'estas', 'eso', 
        'esas', 'esos', 'días', 'horas', 'años', 'meses', 'dicho', 'dicha'
    ])
    
    # Probabilidad mínima para tokens no vistos (usada para suavizado)
    # Se extrae la probabilidad más pequeña (no P_prior) de la clase SPAM.
    prob_minima_spam = min(p for token, p in tabla_prob['SPAM'].items() if token != 'P_prior')
    prob_minima_nospam = min(p for token, p in tabla_prob['NO_SPAM'].items() if token != 'P_prior')
    mensajes_clasificados = {}
    
    # 3. Clasificación usando el método Naive Bayes
    for id_msg, contenido_msg in mensajes_nuevos.items():
        
        tokens = [
            token.lower().strip('.,!?"\'()@#$%\n')
            for token in contenido_msg.split()
            if token.lower().strip('.,!?"\'()@#$%\n') not in stop_words and len(token.strip('.,!?"\'()@#$%\n')) > 2
        ]
        
        puntajes_log = defaultdict(float)
        
        for clase in clases:
            prob_minima_clase = prob_minima_spam if clase == 'SPAM' else prob_minima_nospam
            
            # Iniciar con la Probabilidad A Priori (en logaritmo)
            log_prob_mensaje = np.log(tabla_prob[clase]['P_prior'])
            
            # Multiplicar (sumar en logaritmos) las probabilidades de los tokens
            for token in tokens:
                # Obtener P(token | clase) o usar la probabilidad mínima si el token es nuevo
                prob_token_clase = tabla_prob[clase].get(token, prob_minima_clase)
                log_prob_mensaje += np.log(prob_token_clase)
                
            puntajes_log[clase] = log_prob_mensaje

        # Método de Consenso,el mayor puntaje logarítmico gana
        clase_predicha = max(puntajes_log, key=puntajes_log.get)
        
        mensajes_clasificados[id_msg] = {
            'mensaje': contenido_msg,
            'etiqueta': clase_predicha,
            'puntaje_spam': float(puntajes_log['SPAM']), 
            'puntaje_nospam': float(puntajes_log['NO_SPAM'])
        }
        
        print(f"{id_msg}: Clasificado como {clase_predicha}")
    nombre_archivo_salida = 'etiqueta2.yaml'
    
    try:
        with open(nombre_archivo_salida, 'w', encoding='utf-8') as f:
            yaml.dump(mensajes_clasificados, f)
        
        print(f"Archivo '{nombre_archivo_salida}' creado")
        
    except Exception as e:
        print(f"error: {e}")
        return None
        
    return mensajes_clasificados

clasificacion_final = clasificador_por_consenso()
