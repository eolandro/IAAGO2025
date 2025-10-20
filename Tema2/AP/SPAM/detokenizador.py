from ruamel.yaml import YAML
from collections import defaultdict
import sys

def detokenizador():
    yaml = YAML()
    
    try:
        with open('msg_eti.yaml', 'r', encoding='utf-8') as f:
            mensajes_etiquetados = yaml.load(f)

    except FileNotFoundError:
        print("no se encuentra el archivo msg_eti")
        return None
    except Exception as e:
        print(f"error: {e}")
        return None

    stop_words = set([
        'el', 'la', 'los', 'las', 'un', 'una', 'unos', 'unas', 'de', 'a', 'ante', 
        'bajo', 'con', 'contra', 'en', 'entre', 'hacia', 'hasta', 'para', 'por', 
        'según', 'sin', 'sobre', 'tras', 'y', 'o', 'del', 'al', 'tu', 'su', 'mi', 
        'te', 'que', 'es', 'ha', 'sus', 'sus', 'los', 'que', 'se', 'una', 'un', 
        'suya', 'mio', 'mía', 'mío', 'mi', 'usted', 'eso', 'esto', 'aquello', 'qué',
        'quién', 'como', 'donde', 'cuando', 'este', 'esta', 'estos', 'estas', 'eso', 
        'esas', 'esos', 'días', 'horas', 'años', 'meses', 'dicho', 'dicha'
    ])
    
    conteo_clase = defaultdict(int)
    conteo_token_clase = defaultdict(lambda: defaultdict(int))
    total_tokens_clase = defaultdict(int)
    
    for id_msg, data in mensajes_etiquetados.items():
        clase = data['etiqueta']
        mensaje = data['mensaje']
        conteo_clase[clase] += 1
        tokens = [
            token.lower().strip('.,!?"\'()@#$%\n')
            for token in mensaje.split()
            if token.lower().strip('.,!?"\'()@#$%\n') not in stop_words and len(token.strip('.,!?"\'()@#$%\n')) > 2
        ]
        for token in tokens:
            conteo_token_clase[clase][token] += 1
        
        total_tokens_clase[clase] += len(tokens)

    #Cálculo de Probabilidades (P(token | clase))
    vocabulario = set(t for d in conteo_token_clase.values() for t in d)
    V = len(vocabulario) # Tamaño del vocabulario
    alpha = 1 # Coeficiente de suavizado de Laplace
    
    tabla_prob = {}
    clases = list(conteo_clase.keys())
    
    for clase in clases:
        tabla_prob[clase] = {}
        N_c = total_tokens_clase[clase]
        
        tabla_prob[clase]['P_prior'] = conteo_clase[clase] / len(mensajes_etiquetados)
        
        for token in vocabulario:
            frecuencia_token = conteo_token_clase[clase].get(token, 0)
            
            # Fórmula de Suavizado de Laplace
            prob = (frecuencia_token + alpha) / (N_c + V * alpha)
            tabla_prob[clase][token] = prob

    nombre_archivo_salida = 'tabla_prob.yaml'
    try:
        with open(nombre_archivo_salida, 'w', encoding='utf-8') as f:
            yaml.dump(tabla_prob, f)
        
        print(f"se creo '{nombre_archivo_salida}'")
        print(f"Total de tokens únicos (vocabulario): {V}")
        
    except Exception as e:
        print(f"error{e}")
        return None
        
    return tabla_prob

tabla_conocimiento = detokenizador()

if tabla_conocimiento:
    print("\nEjemplos de probabilidades calculadas:")
    print(f"P(SPAM a priori): {tabla_conocimiento['SPAM']['P_prior']:.4f}")
    print(f"P(NO_SPAM a priori): {tabla_conocimiento['NO_SPAM']['P_prior']:.4f}")
    
    for token in ['premio', 'ganado', 'oportunidad', 'préstamo', 'reclamar', 'dinero']:
        if token in tabla_conocimiento['SPAM']:
             p_spam = tabla_conocimiento['SPAM'].get(token, 0)
             p_nospam = tabla_conocimiento['NO_SPAM'].get(token, 0)
             print(f"P({token} | SPAM): {p_spam:.4f} | P({token} | NO_SPAM): {p_nospam:.4f}")
