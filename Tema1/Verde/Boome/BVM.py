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
        self.Instruccion = ''
        self.C = 0
        self.F = 2
    
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
        
        for fila in self.Mapa:
            for columna in fila:
                Res = Res + f'{columna}'
            Res = Res + '\n'
        
        if (self.F >= 0 and self.F < len(self.Mapa) and 
            self.C >= 0 and self.C < len(self.Mapa[0])):
            self.Mapa[self.F][self.C] = tmp
        return Res
        
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
        self.Instruccion = []
