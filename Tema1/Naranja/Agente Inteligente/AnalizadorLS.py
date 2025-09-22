
import re

# L = [True,String]
# t_nombre_funcion: significa operadores terminales 

def t_numhex(L):
    match L:
        case [A]:
            return [False, A]
        case [A,B]:
            if A:
                if isinstance(B,str) and re.match("#[0-9a-f]{4}",B):
                    return [True,B]
                return [False, B]
            return [False, B]
    return [False,L]

#print(numhex([True,"#111R"]))

def t_operador(L):
    match L:
        case [A]:
            return [False, A]
        case [A,B]:
            if A:
                if B in ['+','-']:
                    return [True,B]
                return [False, B]
            return [False, B]
    return [False,L]

def t_reg(L):
    match L:
        case [A]:
            return [False, A]
        case [A,B]:
            if A:
                if B in ['R0','R1','R2','R3']:
                    return [True,B]
                return [False, B]
            return [False, B]
    return [False,L]


def t_direc(L):
    match L:
        case [A]:
            return [False, A]
        case [A,B]:
            if A:
                if B in ['Izq','Der','Arr','Abj']:
                    return [True,B]
                return [False, B]
            return [False, B]
    return [False,L]

def nt_accion(L):
    match L:
        case ["avanza",D]:
            # R = True o False
            R,V = t_direc([True,D])
            if R:
                return [True,None]
            return [R,V]
    
    return [False,L]

def evalua(L):
    match L:
        case ["sensor",D]:
            # R = True o False
            R,V = t_direc([True,D])
            if R:
                return [True,None]
            return [R,V]
    
    return [False,L]

def opermat(L):
    match L:
        case[Op1,Oper,Op2]:
            # R = True o False
            R,V = t_operador([True,Oper])
            if R:
                # R = True o False
                # V = String que devuelve

                validaciones = [
                    t_numhex([True,Op1]),
                    t_reg([True,Op1]),
                    t_numhex([True,Op2]),
                    t_reg([True,Op2])
                ]
                match validaciones:
                    case [A,B,C,D]:
                        RA,VA = A
                        RB,VB = B
                        RC,VC = C
                        RD,VD = D
                        orden = [str(l) for l in [RA,RB,RC,RD]]
                        match orden:
                            #CASO 1. 2 numeros hexadecimales
                            case ["True","False","True","False"]:
                                return [True,None]
                            #CASO 2. registro y numero hexadecimal
                            case ["False","True","True","False"]:
                                return [True,None]
                            #CASO 3. 2 registros
                            case ["False","True","False","True"]:
                                return [True,None]
                            #CASO 4. numero hexadecimal y registro
                            case ["True","False","False","True"]:
                                return [True,None]
                        return [False,orden]                   
            return [R,V]
    return[False,L]
        
#print(opermat(["R0","+","R1"]))


def asigna(L):
    match L:
        case [R,'=',NH]:
            # RR = True o False
            # RV = String que devuelve
            RR,RV = t_reg([True,R])

            #CASO 1. asginacion de un numero hexadecimal
            RNH,VNH = t_numhex([True,NH])
            if RR and RNH:
                return [True,None]

            #CASO 2. asignacion de un registro
            RNH,VNH = t_reg([True,NH])
            if RR and RNH:
                return [True,None]
        
        #CASO 3. asignacion del resultado de un sensor
        case[R,'=',A,B]:

            # RR, RE = True o False
            # RV, VE = String que devuelve
            RR,RV = t_reg([True,R])
            RE,VE = evalua([A,B])

            if RR and RE:
                return [True,None]
            
        
        case [R,'=',A,B,C]:
            # RR,RR = True o False
            # RV,VO = String que devuelve
            RR,RV = t_reg([True,R])
            RO,VO = opermat([A,B,C])

            if RR and RO:
                return [True,None]

    return [False,L]

#print(asigna(["R0","=","R1",'+','#0111'])) 
#print(asigna(["R0","=",'sensor','Der'])) 


def copi_s(L):
    match L:
        case ["cmp",R]:
            # RG = True o False
            # VG = String que devuelve
            RG,VG = t_reg([True,R])
            if RG:
                return [True,None]
            return [RG,VG]
    return [False,L]

#print(copi_s(['cmp','R3']))


def saltos(L):
    match L:
        case [I,NH]:
            if I in ['Sncero','Scero']:
                RH,VH = t_numhex([True,NH])
                if RH:
                    return [True,None]
                return [False,VH]
            return [False,I]
    return [False,L]

#print(saltos(['Sncero',"#nfff",'+']))

def linea_codigo(STR):
    if isinstance(STR, list):
        STR = " ".join(STR)
    
    if isinstance(STR,str):
        partes = STR.split(" ")

        match partes:
            case [E1,E2]:
                # R = True o False
                # V = Variable que devuelve
                if E1 == 'avanza':
                    R,V = t_direc([True,E2])
                    if R:
                        return [True,None]
                    return [False,V]
                elif E1 == 'cmp':
                    R,V = t_reg([True,E2])
                    if R:
                        return [True,None]
                    return [False,V]
                elif E1 == 'sensor':
                    R,V = t_direc([True,E2])
                    if R:
                        return [True,None]
                    return [False,V]
                else:
                    R,V = saltos([E1,E2])
                    if R:
                        return [True,None]
                    return [False,V]                         
            
            #POSIBLES CASOS DE ASIGNACION
            case [E1,E2,E3]:
                # RA = True o False
                # VA = String que devuelve
                RA,VA = asigna([E1,E2,E3])
                if RA:
                    return [True,None]
                return [False,VA]

            
            case [E1,E2,E3,E4]:
                RA,VA = asigna([E1,E2,E3,E4])
                if RA:
                    return [True,None]
                return [False,VA]
            
            
            case [E1,E2,E3,E4,E5]:
                RA,VA = asigna([E1,E2,E3,E4,E5])
                if RA:
                    return [True,None]
                return [False,VA]
            

        return [False,STR]
            
#print(linea_codigo("avanza Abj"))
#print(linea_codigo("cmp R3"))
#print(linea_codigo("Sncero #ffff"))
#print(linea_codigo("R0 = R1"))
#print(linea_codigo("sensor Der"))

#print((linea_codigo(["R0", "=", "#000a", "+", "#0005"])))
#print((linea_codigo(["R0", "=", "R2", "+", "#0005"])))
#print((linea_codigo(["R0", "=", "R2", "+", "R3"])))
#print((linea_codigo(["R0", "=", "ffff", "+", "R3"])))

    
def programa(L):
    match L:
        # Caso cuando es un programa vacío 
        case []:
            return [True, None] 
        # Caso base: una sola línea
        case [L0]:
            return linea_codigo(L0)
        # Caso recursivo: primera línea + resto del programa
        case [PL, *RL]:
            # R,RR = True o False
            # V,VV = Variable que devuelve
            R, V = linea_codigo(PL)
            if not R:
                return [False, V]
            
            RR, VV = programa(RL)
            if not RR:
                return [False, VV]
            
            return [True, None]
        
    return [False, L]

"""print(programa([
        "R0 = #1234",
        "avanza Der",
        "cmp R0",
        "Sncero #0005"
    ]))"""

#print(programa(["R0 = R3"]))