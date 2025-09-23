import re

class BVM:
    def __init__(self):
        self.R0 = 0
        self.R1 = 0
        self.R2 = 0
        self.R3 = 0
        self.Estado = 'Activo'
        
        self.Mapa =[
            ['1','1','1','1','0','0','1','1','1','1'],
            ['1','1','1','1','0','0','1','1','1','1'],
            ['0','0','0','0','0','0','0','0','0','0'],
            ['0','0','0','0','0','2','0','0','0','0'],
            ['0','0','0','0','0','0','0','0','0','0'],
            ['1','1','1','1','0','0','1','1','1','1'],
            ['1','1','1','1','0','0','1','1','1','1'],
        ]
        self.Instruccion = [] 
        self.C = 0
        self.F = 2
        self.S = 0 
        self.PC = 0 
        self.ZeroFlag = False 
    
    def __str__(self):
        if (self.F < 0 or self.F >= len(self.Mapa) or 
            self.C < 0 or self.C >= len(self.Mapa[0])):
            tmp = ''
        else:
            tmp = self.Mapa[self.F][self.C]
            self.Mapa[self.F][self.C] = 'B' 
            
        Res = ''
        Res = f'R0 : {self.R0}, R1 : {self.R1}, R2 : {self.R2}, R3 : {self.R3} \n'
        Res = Res + f'C : {self.C}, F : {self.F} \n'
        Res = Res + f'Ins : {self.Instruccion} \n'
        Res = Res + f'Estado : {self.Estado} \n'
        Res = Res + f'S : {self.S} \n' 
        Res = Res + f'PC : {self.PC} \n' 
        Res = Res + f'Zero : {self.ZeroFlag} \n' 
        
        for fila in self.Mapa:
            for columna in fila:
                Res = Res + f'{columna}'
            Res = Res + '\n'
        
        if (self.F >= 0 and self.F < len(self.Mapa) and 
            self.C >= 0 and self.C < len(self.Mapa[0])):
            self.Mapa[self.F][self.C] = tmp
        return Res
        
    def _hex_to_int(self, hex_str):
        if re.match("#[0-9a-f]{4}", hex_str):
            return int(hex_str[1:], 16)
        return 0

    def _get_register_value(self, reg_name):
        if reg_name == 'R0': return self.R0
        if reg_name == 'R1': return self.R1
        if reg_name == 'R2': return self.R2
        if reg_name == 'R3': return self.R3
        return 0 

    def _set_register_value(self, reg_name, value):
        if reg_name == 'R0': self.R0 = value
        elif reg_name == 'R1': self.R1 = value
        elif reg_name == 'R2': self.R2 = value
        elif reg_name == 'R3': self.R3 = value

    def ejecutarInstruccion(self):
        if self.Estado == 'Morido':
            return 
       

        match self.Instruccion:
            case ['avanza','Izq']:
                self.C = self.C - 1
                if self.C < 0:
                    self.Estado = 'Morido'
            case ['avanza','Der']:
                self.C = self.C + 1
                if self.C >= len(self.Mapa[0]):  
                    self.Estado = 'Morido'
            case ['avanza','Arr']:
                self.F = self.F - 1
                if self.F < 0:  
                    self.Estado = 'Morido'
            case ['avanza','Abj']:
                self.F = self.F + 1
                if self.F >= len(self.Mapa):  
                    self.Estado = 'Morido'
            
            case ['sensor', direc]:
                target_C, target_F = self.C, self.F
                if direc == 'Izq': target_C -= 1
                elif direc == 'Der': target_C += 1
                elif direc == 'Arr': target_F -= 1
                elif direc == 'Abj': target_F += 1

                if (0 <= target_F < len(self.Mapa) and 
                    0 <= target_C < len(self.Mapa[0])):
                    if self.Mapa[target_F][target_C] in ['0', '2']: 
                        self.S += 1 
                
            case [reg, '=', value]:
                if reg in ['R0', 'R1', 'R2', 'R3']:
                    if value.startswith('#'):
                        self._set_register_value(reg, self._hex_to_int(value))
                    elif value in ['R0', 'R1', 'R2', 'R3']:
                        self._set_register_value(reg, self._get_register_value(value))
            
            case [reg, '=', op1, operator, op2]:
                if reg in ['R0', 'R1', 'R2', 'R3']:
                    val1 = self._hex_to_int(op1) if op1.startswith('#') else self._get_register_value(op1)
                    val2 = self._hex_to_int(op2) if op2.startswith('#') else self._get_register_value(op2)
                    
                    result = 0
                    if operator == '+':
                        result = val1 + val2
                    elif operator == '-':
                        result = val1 - val2
                    
                    self._set_register_value(reg, result)

            case ['cmp', reg]:
                if self._get_register_value(reg) == 0:
                    self.ZeroFlag = True
                else:
                    self.ZeroFlag = False
            
            case ['Sncero', hex_address]:
                if not self.ZeroFlag:
                    self.PC = self._hex_to_int(hex_address) - 1 
            
            case ['Scero', hex_address]:
                if self.ZeroFlag:
                    self.PC = self._hex_to_int(hex_address) - 1 

        self.Instruccion = []
