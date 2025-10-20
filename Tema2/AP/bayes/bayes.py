import numpy as np
from ruamel.yaml import YAML
import sys

class BVM:
    def __init__(self, archivo_config='config_boom.yaml'):
        self.C = 0
        self.F = 0 
        self.Estado = 'Activo'
        self.MAX_INTENTOS = 3
        self.intentos_desactivacion = self.MAX_INTENTOS
        
        config = self._cargar_config(archivo_config)
        self.Mapa = config['mapa']
        self.P_D_dado_B = config['detector']['p_d_dado_b']
        self.P_D_dado_noB = config['detector']['p_d_dado_nob']
        
        self.bomba_pos = self._encontrar_bomba() 
        self.ProbaMap = self._inicializar_probabilidades()
        
    def _cargar_config(self, archivo):
        try:
            yaml = YAML()
            with open(archivo, 'r') as f:
                config_leida = yaml.load(f)
            return config_leida
        except FileNotFoundError:
            print(f"no esta {archivo}")
            sys.exit(1)
        except Exception as e:
            print(f"error: {e}")
            sys.exit(1)
            
    def _encontrar_bomba(self):
        for r in range(len(self.Mapa)):
            for c in range(len(self.Mapa[0])):
                if self.Mapa[r][c] == 2:
                    return (r, c)
        print("No se encontró la bomba.")
        return None

    def _inicializar_probabilidades(self):
        mapa_np = np.array(self.Mapa) 
        casillas_validas = np.sum(mapa_np != 1)
        prob_uniforme = 1.0 / casillas_validas if casillas_validas > 0 else 0
        proba_map = np.where(mapa_np != 1, prob_uniforme, 0.0)
        return proba_map / np.sum(proba_map)

    def imprimir_probabilidad_detector_positivo(self):
        mapa_np = np.array(self.Mapa)
        casillas_validas = np.sum(mapa_np != 1)
        if casillas_validas == 0: return
        p_prior_bomba = 1.0 / casillas_validas
        p_prior_no_bomba = 1.0 - p_prior_bomba
        p_d_dado_b = self.P_D_dado_B
        p_d_dado_nob = self.P_D_dado_noB
        numerador = p_d_dado_b * p_prior_bomba
        denominador = (p_d_dado_b * p_prior_bomba) + (p_d_dado_nob * p_prior_no_bomba)
        if denominador == 0: return
        p_bomba_dado_d = numerador / denominador
        print(f"Probabilidad a priori (P(B)) por celda: 1/{casillas_validas} = {p_prior_bomba:.4f}")
        print(f"Probabilidad del detector positivo dada la bomba (P(D|B)): {p_d_dado_b}")
        print(f"Probabilidad del detector positivo sin bomba (P(D|¬B)): {p_d_dado_nob}")
        print("-" * 35)
        print(f"La probabilidad de Bayes de que la bomba esté en una celda tras un detector positivo es: {p_bomba_dado_d:.4f}")
        print("-" * 35)
        
    def simular_lectura_detector(self):
        es_posicion_bomba = (self.F, self.C) == self.bomba_pos
        prob_positivo = self.P_D_dado_B if es_posicion_bomba else self.P_D_dado_noB
        return np.random.choice([True, False], p=[prob_positivo, 1 - prob_positivo])

    def calcular_likelihood(self, r, c, F_obs, C_obs, lectura_positiva):
        es_hipotesis_en_celda_observada = (r == F_obs and c == C_obs)
        if lectura_positiva:
            return self.P_D_dado_B if es_hipotesis_en_celda_observada else self.P_D_dado_noB
        else:
            return (1 - self.P_D_dado_B) if es_hipotesis_en_celda_observada else (1 - self.P_D_dado_noB)

    def ejecutar_detector_bayes(self, F_obs, C_obs, lectura_positiva):
        if self.Estado in ['Morido', 'Victoria']: return

        likelihood_map = np.zeros_like(self.ProbaMap)
        for r in range(likelihood_map.shape[0]):
            for c in range(likelihood_map.shape[1]):
                if self.Mapa[r][c] != 1:
                    likelihood_map[r, c] = self.calcular_likelihood(r, c, F_obs, C_obs, lectura_positiva)
        
        nuevo_mapa_proba = likelihood_map * self.ProbaMap
        suma_total = np.sum(nuevo_mapa_proba)
        if suma_total > 0: self.ProbaMap = nuevo_mapa_proba / suma_total
        
        resultado_lectura = "POSITIVA" if lectura_positiva else "NEGATIVA"
        max_prob = np.max(self.ProbaMap)
        max_pos = np.unravel_index(np.argmax(self.ProbaMap), self.ProbaMap.shape)
        print(f"   -> Lectura {resultado_lectura} en ({F_obs}, {C_obs}) actualizada. Max P: {max_prob:.4f} en {max_pos}")

    def __str__(self):
        mapa_display = np.array(self.Mapa, dtype=str)
        if self.Estado == 'Activo':
            mapa_display[self.F, self.C] = 'R'
        Res = f'Posición: F: {self.F}, C: {self.C} \n'
        Res += f'Intentos de Desactivación: {self.intentos_desactivacion}/{self.MAX_INTENTOS} \n'
        Res += f'Estado: {self.Estado} \n'
        Res += f'Posición Real Bomba: {self.bomba_pos}\n'
        Res += '\n--- POSICIÓN ACTUAL ---\n'
        for fila in mapa_display:
            Res += ' '.join(f"{celda:^3}" for celda in fila) + '\n'
        Res += '\n--- MAPA DE PROBABILIDADES ---\n'
        for r in range(self.ProbaMap.shape[0]):
            Res += " ".join([f"{p:.4f}" for p in self.ProbaMap[r]]) + "\n"
        return Res

def crear_recorrido_barrido(mapa):
    recorrido = []
    filas, columnas = len(mapa), len(mapa[0])
    for fila in range(filas):
        rango_columnas = range(columnas) if fila % 2 == 0 else range(columnas - 1, -1, -1)
        for columna in rango_columnas:
            if mapa[fila][columna] != 1:
                recorrido.append((fila, columna))
    return recorrido

if __name__ == "__main__":
    vm = BVM()
    vm.imprimir_probabilidad_detector_positivo()
    recorrido_barrido = crear_recorrido_barrido(vm.Mapa)
    print(vm)

    UMBRAL_RIESGO = 0.95
    UMBRAL_EXPLOTACION = 0.30
    
    pos_actual_recorrido = 0
    while pos_actual_recorrido < len(recorrido_barrido) and vm.Estado == 'Activo':
        
        max_prob_global = np.max(vm.ProbaMap)
        F_max, C_max = np.unravel_index(np.argmax(vm.ProbaMap), vm.ProbaMap.shape)
        
        if max_prob_global >= UMBRAL_EXPLOTACION and (vm.F, vm.C) != (F_max, C_max):
            F_siguiente, C_siguiente = F_max, C_max
            print(f"[ESTRATEGIA] Desviando a celda más probable: ({F_max}, {C_max}) con P={max_prob_global:.4f}")
        else:
            F_siguiente, C_siguiente = recorrido_barrido[pos_actual_recorrido]
            pos_actual_recorrido += 1

        print(f"\n==================== MOVIÉNDOSE A ({F_siguiente}, {C_siguiente}) ====================")
        vm.F, vm.C = F_siguiente, C_siguiente

        print(f"FASE 1: Tomando lectura inicial en la celda actual...")
        lectura_inicial = vm.simular_lectura_detector()
        vm.ejecutar_detector_bayes(vm.F, vm.C, lectura_inicial)

        if lectura_inicial:
            print(f"[ALERTA] Lectura positiva. Verificando la celda ({vm.F}, {vm.C}) con más lecturas.")
            for i in range(4):
                if vm.Estado != 'Activo': break
                print(f"FASE 2: Tomando lectura de confirmación {i+1}/4...")
                lectura_confirmatoria = vm.simular_lectura_detector()
                vm.ejecutar_detector_bayes(vm.F, vm.C, lectura_confirmatoria)

        max_prob_final = np.max(vm.ProbaMap)
        F_max_final, C_max_final = np.unravel_index(np.argmax(vm.ProbaMap), vm.ProbaMap.shape)

        if max_prob_final >= UMBRAL_RIESGO and (vm.F, vm.C) == (F_max_final, C_max_final):
            if vm.intentos_desactivacion > 0:
                vm.intentos_desactivacion -= 1
                print(f"[DECISIÓN] P={max_prob_final:.4f} >= {UMBRAL_RIESGO}. ¡INTENTANDO DESACTIVACIÓN! Restantes: {vm.intentos_desactivacion}")
                if (vm.F, vm.C) == vm.bomba_pos:
                    vm.Estado = 'Victoria'
                    print("¡VICTORIA! La bomba fue desactivada exitosamente.")
                else:
                    vm.ProbaMap[vm.F, vm.C] = 0.0
                    vm.ProbaMap /= np.sum(vm.ProbaMap)
                    print("¡FALLO! Intento gastado en celda vacía.")
            
            if vm.intentos_desactivacion <= 0 and vm.Estado != 'Victoria':
                vm.Estado = 'Morido'
                print("¡GAME OVER! Se acabaron los intentos.")
        else:
            print(f"[EXPLORACIÓN] Probabilidad máxima ({max_prob_final:.4f}) no es suficiente o está en otra celda. Se continúa explorando.")

    print("\n" + "="*40)
    print("FIN DE LA SIMULACIÓN")
    print("="*40)
    print(vm)
