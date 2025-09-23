import re

class BVM:
    def __init__(self):
        self.R0 = 0
        self.R1 = 0
        self.R2 = 0
        self.R3 = 0
        self.Estado = 'Activo'
        
        self.Mapa = [
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
        tmp = ''
        if (0 <= self.F < len(self.Mapa) and 0 <= self.C < len(self.Mapa[0])):
            tmp = self.Mapa[self.F][self.C]
            self.Mapa[self.F][self.C] = 'B'
        
        Res = f"Registros: R0={self.R0}, R1={self.R1}, R2={self.R2}, R3={self.R3}\n"
        Res += f"Posición Boome: Fila={self.F}, Columna={self.C}\n"
        Res += f"(S): {self.S}\n"
        Res += f"Estado: {self.Estado}\n"
        Res += f"PC: {self.PC}"
        Res += "Mapa (1=obstáculo, 0=libre, 2=objetivo, B=Boome):\n"
        
        for fila in self.Mapa:
            Res += ' '.join(fila) + '\n'
        
        if tmp:
            self.Mapa[self.F][self.C] = tmp
        return Res

    def _hex_to_int(self, hex_str):
        if isinstance(hex_str, str) and re.match(r"#[0-9a-fA-F]{4}", hex_str):
            return int(hex_str[1:], 16)
        return 0

    def _get_register_value(self, reg_name):
        if reg_name == 'R0': return self.R0
        if reg_name == 'R1': return self.R1
        if reg_name == 'R2': return self.R2
        if reg_name == 'R3': return self.R3
        return 0

    def _set_register_value(self, reg_name, value):
        clamped = max(0, value)
        if reg_name == 'R0': self.R0 = clamped
        elif reg_name == 'R1': self.R1 = clamped
        elif reg_name == 'R2': self.R2 = clamped
        elif reg_name == 'R3': self.R3 = clamped

    def _check_collision(self, new_F, new_C):
        if (0 <= new_F < len(self.Mapa) and 0 <= new_C < len(self.Mapa[0])):
            return self.Mapa[new_F][new_C] != '1'
        return False

    def ejecutarInstruccion(self):
        if self.Estado != 'Activo':
            return

        match self.Instruccion:
            case ['avanza', 'Izq']:
                new_C = self.C - 1
                if self._check_collision(self.F, new_C):
                    self.C = new_C
                    self.S = 0
                else:
                    self.Estado = 'Morido'
            case ['avanza', 'Der']:
                new_C = self.C + 1
                if self._check_collision(self.F, new_C):
                    self.C = new_C
                    self.S = 0
                else:
                    self.Estado = 'Morido'
            case ['avanza', 'Arr']:
                new_F = self.F - 1
                if self._check_collision(new_F, self.C):
                    self.F = new_F
                    self.S = 0
                else:
                    self.Estado = 'Morido'
            case ['avanza', 'Abj']:
                new_F = self.F + 1
                if self._check_collision(new_F, self.C):
                    self.F = new_F
                    self.S = 0
                else:
                    self.Estado = 'Morido'

            case ['sensor', direc]:
                target_F, target_C = self.F, self.C
                if direc == 'Izq': target_C -= 1
                elif direc == 'Der': target_C += 1
                elif direc == 'Arr': target_F -= 1
                elif direc == 'Abj': target_F += 1

                dentro_limites = (0 <= target_F < len(self.Mapa) and 0 <= target_C < len(self.Mapa[0]))
                if not dentro_limites or (dentro_limites and self.Mapa[target_F][target_C] in ['1', '2']):
                    self.S = 1
                else:
                    self.S = 0

            case [reg, '=', value]:
                if reg in ['R0', 'R1', 'R2', 'R3']:
                    if value.startswith('#'):
                        self._set_register_value(reg, self._hex_to_int(value))
                    elif value in ['R0', 'R1', 'R2', 'R3']:
                        self._set_register_value(reg, self._get_register_value(value))

            case [reg, '=', op1, oper, op2]:
                if reg in ['R0', 'R1', 'R2', 'R3']:
                    val1 = self._hex_to_int(op1) if op1.startswith('#') else self._get_register_value(op1)
                    val2 = self._hex_to_int(op2) if op2.startswith('#') else self._get_register_value(op2)
                    result = val1 + val2 if oper == '+' else val1 - val2 if oper == '-' else 0
                    self._set_register_value(reg, result)

            case ['cmp', reg]:
                self.ZeroFlag = (self._get_register_value(reg) == 0)

            case ['Sncero', hex_address]:
                if not self.ZeroFlag:
                    self.PC = self._hex_to_int(hex_address) - 1

            case ['Scero', hex_address]:
                if self.ZeroFlag:
                    self.PC = self._hex_to_int(hex_address) - 1

        self.Instruccion = []
