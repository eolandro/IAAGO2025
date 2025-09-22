
class BVM:
    def __init__(self):
        # R -> registros
        self.R0 = 0
        self.R1 = 0
        self.R2 = 0
        self.R3 = 0
        self.S = 0 
        # 0 -> lugar disponible
        # 1 -> fuera de mapa
        # 2 -> obstruccion
        self.mapa = [
            ['1','1','1','1','0','0','1','1','1','1'],
            ['1','1','1','1','0','0','1','1','1','1'],
            ['0','0','0','0','0','0','0','0','0','0'],
            ['0','0','0','0','0','2','0','0','0','0'],
            ['0','0','0','0','0','0','0','0','0','0'],
            ['1','1','1','1','0','0','1','1','1','1'],
            ['1','1','1','1','0','0','1','1','1','1']
        ]
        self.instruccion = ''
        self.columna = 0
        self.fila = 2
        self.estado = 'Activo'
        self.programa = []  
        self.contador_programa = 0
        self.ejecutando = True

    def __str__(self):
        #res -> registros
        tmp = ''
        if self.estado != 'Morido':
            tmp = self.mapa[self.fila][self.columna]
            self.mapa[self.fila][self.columna]  = 'B'

        res = ''
        res += f'\nREGISTROS:\n'
        res += f'R0: {self.R0} | R1: {self.R1} | R2: {self.R2} | R3: {self.R3} | S: {self.S}\n'
        res += f'POSICIÓN: Columna={self.columna}, Fila={self.fila}\n'
        res += f'ESTADO: {self.estado}\n'
        res += f'\nMAPA:\n'
            
        for fila in self.mapa:
            for columna in fila:
                res = res + f'{columna}'
            res = res + '\n'
            
        if self.estado!='Morido':
            self.mapa[self.fila][self.columna] = tmp
            
        return res
        
    def hex_a_decimal(self, hex_str):
        if hex_str.startswith('#'):
            hex_str = hex_str[1:]
        return int(hex_str, 16)
    
    def realizar_operacion(self, op1, operador, op2):

        if isinstance(op1, str) and op1.startswith('#'):
            op1 = self.hex_a_decimal(op1)
        if isinstance(op2, str) and op2.startswith('#'):
            op2 = self.hex_a_decimal(op2)
            
        # Realizar operación
        if operador == '+':
            return op1 + op2
        elif operador == '-':
            return op1 - op2
        else:
            return 0
    
    def obtener_valor_registro(self, registro):
        if registro == "R0":
            return self.R0
        elif registro == "R1":
            return self.R1
        elif registro == "R2":
            return self.R2
        elif registro == "R3":
            return self.R3
        elif registro.startswith('#'):  # Es un hexadecimal
            return self.hex_a_decimal(registro)
        return 0
    
    def asignar_valor_registro(self, registro, valor):
        if registro == "R0":
            self.R0 = valor
        elif registro == "R1":
            self.R1 = valor
        elif registro == "R2":
            self.R2 = valor
        elif registro == "R3":
            self.R3 = valor
    
    def leer_sensor(self, direccion):
        fila_temp, columna_temp = self.fila, self.columna
        
        # Calcular posición adyacente
        if direccion == "Izq":
            columna_temp -= 1
        elif direccion == "Der":
            columna_temp += 1
        elif direccion == "Arr":
            fila_temp -= 1
        elif direccion == "Abj":
            fila_temp += 1
        
        # Verificar si está fuera del mapa
        if (fila_temp < 0 or fila_temp >= len(self.mapa) or 
            columna_temp < 0 or columna_temp >= len(self.mapa[0])):
            return 1  # Fuera de mapa
        
        valor_celda = self.mapa[fila_temp][columna_temp]
        
        if valor_celda == '0':
            return 0
        else:
            return 1
    
    def ejecutar_instruccion(self):
        if self.estado == 'Morido':
            return 
        
        # Verificar que tenemos una instrucción válida
        if not self.instruccion or len(self.instruccion) < 2:
            return
            
        # INSTRUCCIONES DE MOVIMIENTO 
        if self.instruccion[0] == "avanza":
            if self.instruccion[1] == "Izq":
                self.columna -= 1
                if self.columna < 0:
                    self.estado = 'Morido'
                elif self.mapa[self.fila][self.columna] == '1':  # fuera de mapa
                    self.estado = 'Morido'
                elif self.mapa[self.fila][self.columna] == '2':  # obstrucción
                    self.estado = 'Morido'
                    
            elif self.instruccion[1] == "Der":
                self.columna += 1
                if self.columna >= len(self.mapa[0]):  
                    self.estado = 'Morido'
                elif self.mapa[self.fila][self.columna] == '1':  # fuera de mapa
                    self.estado = 'Morido'
                elif self.mapa[self.fila][self.columna] == '2':  # obstrucción
                    self.estado = 'Morido'
                    
            elif self.instruccion[1] == "Arr":
                self.fila -= 1
                if self.fila < 0:
                    self.estado = 'Morido'
                elif self.mapa[self.fila][self.columna] == '1':  # fuera de mapa
                    self.estado = 'Morido'
                elif self.mapa[self.fila][self.columna] == '2':  # obstrucción
                    self.estado = 'Morido'
                    
            elif self.instruccion[1] == "Abj":
                self.fila += 1
                if self.fila >= len(self.mapa):  
                    self.estado = 'Morido'
                elif self.mapa[self.fila][self.columna] == '1':  # fuera de mapa
                    self.estado = 'Morido'
                elif self.mapa[self.fila][self.columna] == '2':  # obstrucción
                    self.estado = 'Morido'
        
        # ASIGNACIONES SIMPLES 
        elif len(self.instruccion) == 3 and self.instruccion[1] == "=":

            registro_destino = self.instruccion[0]
            valor_fuente = self.instruccion[2]
           
            valor = self.obtener_valor_registro(valor_fuente)
            
            self.asignar_valor_registro(registro_destino, valor)

        #ASIGNACIONES CON SENSOR EN S
        if len(self.instruccion) == 2 and self.instruccion[0] == 'sensor':
            
            direccion = self.instruccion[1]
            valor_sensor = self.leer_sensor(direccion)

            self.S = valor_sensor  
            
        # ASIGNACIONES CON SENSOR EN REGISTROS
        elif len(self.instruccion) == 4 and self.instruccion[1] == "=":
            
            if self.instruccion[2] == "sensor":
                registro = self.instruccion[0]
                direccion = self.instruccion[3]
                
                valor_sensor = self.leer_sensor(direccion)

                self.asignar_valor_registro(registro,valor_sensor)
        
        # ASIGNACIONES CON OPERACIONES MATEMÁTICAS 
        elif len(self.instruccion) == 5 and self.instruccion[1] == "=":
            
            registro_destino = self.instruccion[0]
            operando1 = self.instruccion[2]
            operador = self.instruccion[3]
            operando2 = self.instruccion[4]
            
            valor1 = self.obtener_valor_registro(operando1)
            valor2 = self.obtener_valor_registro(operando2)
            
            resultado = self.realizar_operacion(valor1, operador, valor2)
            
            self.asignar_valor_registro(registro_destino, resultado)
        
        # COMPARACIONES 
        elif self.instruccion[0] == "cmp":
            if len(self.instruccion) >= 2:
                registro = self.instruccion[1]
                valor = self.obtener_valor_registro(registro)
                self.S = valor 
        
        # SALTOS 
        elif self.instruccion[0] in ["Scero", "Sncero"]:
             if len(self.instruccion) >= 2:
                direccion_salto = self.instruccion[1]
                linea_destino = self.hex_a_decimal(direccion_salto) - 1
                
                if self.instruccion[0] == "Scero":
                    if self.S == 0:
                        if 0 <= linea_destino < len(self.programa):
                            self.contador_programa = linea_destino - 1  

                elif self.instruccion[0] == "Sncero":
                    if self.S != 0:
                        if 0 <= linea_destino < len(self.programa):
                            self.contador_programa = linea_destino - 1 
                
        self.instruccion = []

    def cargar_programa(self, lineas):
        self.programa = [linea.strip() for linea in lineas if linea.strip()]
        self.contador_programa = 0
        self.ejecutando = True

    def ejecutar(self):
        
        while self.ejecutando and self.contador_programa < len(self.programa) and self.estado != 'Morido':
            
            linea_actual = self.programa[self.contador_programa]
            L = [l for l in linea_actual.split(' ') if l]
            
            print('='*50)
            print(f'\nLínea {self.contador_programa+1}: {L}')
            
            self.instruccion = L
            self.ejecutar_instruccion()
            print(self)
            #print('='*50)
            #print('\n')
            
            self.contador_programa += 1 
