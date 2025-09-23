import re

def t_numhex(L):#L = [True,String]
    match L:
        case [A]:
            return [False,A]
        case[A,B]:
            if A:
                if isinstance(B,str) and re.match('#[0-9a-f]{4}',B):
                    return [True, B]
                return [False, B]
            return [False, B]
    return [False, L]

def t_operador(L):
    match L:
        case [A]:
            return [False,A] 
        case[A,B]:
            if A:
                if B in ['+','-']:
                    return [True, B]
                return [False, B]
            return [False, B]
    return [False, L]   

def t_reg(L):
    match L:
        case [A]:
            return [False,A] 
        case[A,B]:
            if A:
                if B in ['R0','R1','R2','R3']:
                    return [True, B]
                return [False, B]
            return [False, B]
    return [False, L]   

def t_direc(L):
    match L:
        case [A]:
            return [False,A] 
        case[A,B]:
            if A:
                if B in ['Izq','Der', 'Arr', 'Abj']:
                    return [True, B]
                return [False, B]
            return [False, B]
    return [False, L]   

def accion(L):
    match L:
        case["avanza",D]:
            R,V =t_direc([True,D])
            if R:
                return [True,None]
            return [R,V]
    return [False, L]
#me
def evalua(L):
    match L:
        case["sensor",D]:
            R,V =t_direc([True,D])
            if R:
                return [True,None]
            return [R,V]
    return [False, L]

def opermat(L):
    match L:
        case [Op1,Oper,Op2]:
            R,V= t_operador([True, Oper])
            if R:
                LL= [
                    t_numhex([True,Op1]),
                    t_reg([True,Op1]),
                    t_numhex([True,Op2]),
                    t_reg([True,Op2])

                ]
                match LL:
                    case [A,B,C,D]:
                        RA,VA=A
                        RB,VB=B
                        RC,VC=C
                        RD,VD=D
                        LLL=[str(l) for l in [RA,RB,RC,RD]]
                        match LLL:
                            case ["True","False","True","False"]:
                                return [True,None]
                            case["False","True","True","False"]:
                                return [True,None]
                            case["False","True","False","True"]:
                                return [True,None]
                            case ["True","False","False","True"]:
                                return [True,None]
                        return [False,LLL]

                #return [True,None]
                # return [True,None]
            return [R,V]
    return [False,L]

def asigna(L):
    match L:
        case [R ,"=", NH]:
            RR,RV= t_reg([True,R])
            RNH,VNH= t_numhex([True,NH])
            if RR and RNH:
                return [True,None]
                
            RNH,VNH = t_reg([True,NH])
            if RR and RNH:
                return [True,None]
        
        case [R, '=',A,B]:
            RR,RV=t_reg([True,R])
            RE,VE =evalua([A,B])
            if RR and RE:
                return[True,None]
        #me
        case [R, "=", A, B, C]:
            RR, RV = t_reg([True, R])
            RRO, RVO = opermat([A, B, C])
            if RR and RRO:
                return [True, None]

    return [False, L]

def copi_s(L):
    match L:
        case ["cmp", R]:
            RR, VR = t_reg([True, R])
            if RR:
                return [True, None]
            return [RR, VR]
    return [False, L]

def saltos(L):
    match L:
        case ["Sncero", HH]:
            R, V = t_numhex([True, HH])
            if R:
                return [True, None]
            return [R, V]
        case ["Scero", HH]:
            R, V = t_numhex([True, HH])
            if R:
                return [True, None]
            return [R, V]
    return [False, L]

"""def linea_codigo(STR):
    if not isinstance(STR, str):
        return [False, STR]
    LS = STR.split(" ")
    for f in [accion, asigna, copi_s, saltos]:
        R, V = f(LS)
        if R:
            return [True, None]
    return [False, STR]
"""
def programa(L):
    match L:
        case [L0]:
            return linea_codigo(L0)
        case [PL, *RL]:
            R1, V1 = linea_codigo(PL)
            if R1:
                return programa(RL)
            return [False, PL]
    return [False, L]

def linea_codigo(L):
    match L:
        case ['avanza', B]:
            R, V = accion(['avanza', B])
            if not R:
                print(f"Error: dirección inválida '{V}' en instrucción {L}")
                return False
            return True

        case ['sensor', D]:
            R, V = evalua(['sensor', D])
            if not R:
                print(f"Error: dirección inválida '{V}' en instrucción {L}")
                return False
            return True

        case [R, '=', *args]:
            R2, V2 = asigna([R, '=', *args])
            if not R2:
                print(f"Error: asignación inválida '{V2}' en instrucción {L}")
                return False
            return True

        case ['cmp', R]:
            R3, V3 = copi_s(['cmp', R])
            if not R3:
                print(f"Error: registro inválido '{V3}' en instrucción {L}")
                return False
            return True

        case ['Scero', HH] | ['Sncero', HH]:
            R4, V4 = saltos([L[0], HH])
            if not R4:
                print(f"Error: salto inválido '{V4}' en instrucción {L}")
                return False
            return True

        case _:
            print(f"Error: instrucción desconocida {L}")
            return False

#print(t_numhex([True,"#1111"]))
#print(t_numhex([True,"0x1111"]))
#print(opermat(["#0001", "+", "R1"]))