class BVM:
    def __init__(self,pc=0):

        self.R0=0
        self.R1=0
        self.R2=0
        self.R3=0

        self.Mapa=[
            ['1','1','1','1','0','0','1','1','1','1'],
            ['1','1','1','1','0','0','1','1','1','1'],
            ['0','0','0','0','0','0','0','0','0','0'],
            ['0','0','0','0','0','2','0','0','0','0'],
            ['0','0','0','0','0','0','0','0','0','0'],
            ['1','1','1','1','0','0','1','1','1','1'],
            ['1','1','1','1','0','0','1','1','1','1']
            ]
        #ACCESO Self.Registro[0][0]
        self.Registros=[
            [ 'R0','R1','R2','R3'],
            [self.R0, self.R1, self.R2, self.R3]
        ]
        
        #Bommie
        self.Instruccion = []
        self.C=0
        self.F=2
        self.Estado='Activo'

        self.S=0
        #linea de programa
        self.PC=pc
    
    def __str__(self):
        tmp = ''
        if self.Estado != 'Morido':    
            tmp = self.Mapa[self.F][self.C]
            self.Mapa[self.F][self.C] = 'B'

        Res= ''
        Res = Res +f'R0 :{self.R0}, R1:{self.R1}, R2 :{self.R2}, R3:{self.R3} \n'
        Res = Res+ f'C: {self.C}, F:{self.F} \n'
        Res = Res + f'Ins:{self.Instruccion}\n'
        Res = Res + f'Estado:{self.Estado}\n'
        Res = Res + f'Valor Salto:{self.S}\n'


        for fila in self.Mapa:
            for columna in fila:
                Res = Res + f'{columna} '
            Res = Res + '\n'


        if self.Estado != 'Morido':
            self.Mapa[self.F][self.C] = tmp
        return Res
    
    def reasignar_valor(self):
        for columna in range(len(self.Registros[0])):
            if columna == 0 :
                self.R0= self.Registros[1][columna]
            elif columna == 1 :
                self.R1= self.Registros[1][columna]
            elif columna == 2 :
                self.R2= self.Registros[1][columna]
            elif columna == 3 :
                self.R3= self.Registros[1][columna]

        print(self.R0,self.R1,self.R2,self.R3)    

    def ejecutarInstruccion(self,R1=None,R2=None,R3=None):
        if self.Estado == 'Morido':
            return

        match self.Instruccion:
            case ['avanza','Izq']:
                self.C = self.C - 1
                if self.C < 0 or self.Mapa[self.F][self.C] == '1':
                    self.Estado = 'Morido'

            case ['avanza','Der']:
                self.C = self.C + 1
                if self.C >= len(self.Mapa[self.F]) or self.Mapa[self.F][self.C] == '1':
                    self.Estado = 'Morido'

            case ['avanza','Arr']:
                self.F = self.F - 1
                if self.F < 0 or self.Mapa[self.F][self.C] == '1':
                    self.Estado = 'Morido'

            case ['avanza','Abj']:
                self.F = self.F + 1
                if self.F >= len(self.Mapa) or self.Mapa[self.F][self.C] == '1':
                    self.Estado = 'Morido'
    
            case ['sensor','Der']:
                self.S = 0
                if self.C+1 >= len(self.Mapa[self.F]) or self.Mapa[self.F][self.C+1] != '0':
                    self.S = 1
                else:
                    self.S = 0

            case ['sensor','Abj']:
                self.S = 0
                if self.F+1 >= len(self.Mapa) or self.Mapa[self.F+1][self.C] != '0':
                    self.S = 1
                else:
                    self.S = 0    
            
            case ['sensor','Izq']:
                self.S = 0
                if self.C-1 < 0 or self.Mapa[self.F][self.C-1] != '0':
                    self.S = 1
                else:
                    self.S = 0
            
            case ['sensor','Arr']:
                self.S = 0
                if self.F - 1 >= 0 and self.Mapa[self.F - 1][self.C] != '0':
                    self.S = 1
                else:
                    self.S = 0  
            

            case ['Scero', HH]:
                Linea = int(HH[1:],16)-1
                if self.S == 0:
                    self.PC = Linea
                else:
                    self.PC += 1

            case ['Sncero', HH]:
                Linea = int(HH[1:], 16) - 1
                if self.S != 0:
                    self.PC = Linea
                else:
                    self.PC += 1
            
            case [R1, '=', op1, operador, op2]:
                if R1 is not None and op1 is not None and op2 is not None:
                    for columna in range(len(self.Registros[0])):  # busca R1
                        if self.Registros[0][columna] == R1:
                            # obtener valor de op1
                            for columna2 in range(len(self.Registros[0])):
                                if self.Registros[0][columna2] == op1:
                                    val_op1 = self.Registros[1][columna2]
                                    break
                            else:  
                                val_op1 = int(op1[1:], 16)

                            # obtener valor de op2
                            for columna3 in range(len(self.Registros[0])):
                                if self.Registros[0][columna3] == op2:
                                    val_op2 = self.Registros[1][columna3]
                                    break
                            else:  
                                val_op2 = int(op2[1:], 16)

                            # operación
                            if operador == '+':
                                self.Registros[1][columna] = val_op1 + val_op2
                            elif operador == '-':
                                self.Registros[1][columna] = val_op1 - val_op2

                    self.reasignar_valor()
                
            case [R1, '=', numhex]:
                if R1 is not None and numhex is not None:
                    for columna in range(len(self.Registros[0])):
                        if self.Registros[0][columna] == R1:
                            self.Registros[1][columna] = int(numhex[1:], 16)
                    self.reasignar_valor()

            case [R1, '=', R2]:
                if R1 !=None and R2 !=None:            
                    for columna in range(len(self.Registros[0])):
                        #print(f'fila {self.Registros[0][columna]} valor: {self.Registros[1][columna]}')
                        if self.Registros[0][columna] == R1:   
                            #print(f'#OR fila {self.Registros[0][columna]} valor: {self.Registros[1][columna]}')
                            #self.Registros[1][columna]         
                            for columna2 in range(len(self.Registros[0])):
                                if self.Registros[0][columna2] == R2: 
                                    self.Registros[1][columna] = self.Registros[1][columna2]
                                    #print(f'#DES fila {self.Registros[0][columna]} valor: {self.Registros[1][columna]}')
                    self.reasignar_valor()
                elif R1 != None and R2 == None:
                    print("Falta Asignar Valor al registro ", R1)
                elif R1 == None and R2 != None:
                    print("Falta Asignar Valor al registro", R2)
                #self.Instruccion = []

#            case [R1, '=', R2, operador, op]:
 #               if R1 != None and R2 != None:
   #                 for columna in range(len(self.Registros[0])):
  #                      if self.Registros[0][columna] == R1:
    #                        for columna2 in range(len(self.Registros[0])):
    #                            if self.Registros[0][columna2] == R2:
     #                               val_op2 = int(op[1:], 16)  # convertimos el inmediato
     #                               if operador == '+':
      #                                  self.Registros[1][columna] = self.Registros[1][columna2] + val_op2
       #                             elif operador == '-':
        #                                self.Registros[1][columna] = self.Registros[1][columna2] - val_op2
         #           self.reasignar_valor()
                    
            
            case ["cmp", R]:
                if R in self.Registros[0]:  # si R es un registro válido
                    for columna in range(len(self.Registros[0])):
                        if self.Registros[0][columna] == R:
                            if self.Registros[1][columna] == 0:
                                self.S = 0   # registro == 0
                            else:
                                self.S = 1   # registro != 0


vm=BVM()
vm.ejecutarInstruccion()
print(vm)
