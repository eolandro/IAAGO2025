import re

def t_numhex(L):
    match L:
        case [A]:
            return [False, A]
        case [A, B]:
            if A:
                if isinstance(B, str) and re.match(r"#[0-9a-fA-F]{4}", B):
                    return [True, B]
                return [False, B]
            return [False, B]
    return [False, L]

def t_operador(L):
    match L:
        case [A]:
            return [False, A]
        case [A, B]:
            if A:
                if B in ['+', '-']:
                    return [True, B]
                return [False, B]
            return [False, B]
    return [False, L]

def t_reg(L):
    match L:
        case [A]:
            return [False, A]
        case [A, B]:
            if A:
                if B in ['R0', 'R1', 'R2', 'R3']:
                    return [True, B]
                return [False, B]
            return [False, B]
    return [False, L]

def t_direc(L):
    match L:
        case [A]:
            return [False, A]
        case [A, B]:
            if A:
                if B in ['Izq', 'Der', 'Arr', 'Abj']:
                    return [True, B]
                return [False, B]
            return [False, B]
    return [False, L]

def accion(L):
    match L:
        case ["avanza", D]:
            R, V = t_direc([True, D])
            if R:
                return [True, None]
            return [R, V]
    return [False, L]

def evalua(L):
    match L:
        case ["sensor", D]:
            R, V = t_direc([True, D])
            return [R, V]
    return [False, L]

def opermat(L):
    match L:
        case [Op1, Oper, Op2]:
            R, V = t_operador([True, Oper])
            if R:
                LL = [
                    t_numhex([True, Op1]), t_reg([True, Op1]),
                    t_numhex([True, Op2]), t_reg([True, Op2])
                ]
                match LL:
                    case [A, _, C, _] if A[0] or C[0]:
                        return [True, None]
                return [False, LL]
            return [R, V]
    return [False, L]

def asigna(L):
    match L:
        case [R, "=", NH]:
            RR, RV = t_reg([True, R])
            RNH, VNH = t_numhex([True, NH])
            if RR and RNH:
                return [True, None]
            RNH, VNH = t_reg([True, NH])
            if RR and RNH:
                return [True, None]
                
        case [R, "=", A, B, C]:
            RR, RV = t_reg([True, R])
            if not RR:
                return [False, L]
            ROP, VOP = opermat([A, B, C])
            if ROP:
                return [True, None]
                
    return [False, L]

def copi_s(L):
    match L:
        case ["cmp", R]:
            RR, RV = t_reg([True, R])
            if RR:
                return [True, None]
    return [False, L]

def saltos(L):
    match L:
        case ["Sncero", HH] | ["Scero", HH]:
            R, V = t_numhex([True, HH])
            if R:
                return [True, None]
    return [False, L]

def linea_codigo(LS):
    if not isinstance(LS, list):
        return [False, LS]
    
    R_asigna, V_asigna = asigna(LS)
    if R_asigna:
        return [True, None]
    
    R_copi, V_copi = copi_s(LS)
    if R_copi:
        return [True, None]
    
    R_saltos, V_saltos = saltos(LS)
    if R_saltos:
        return [True, None]
    
    R_accion, V_accion = accion(LS)
    if R_accion:
        return [True, None]
    
    R_evalua, V_evalua = evalua(LS)
    if R_evalua:
        return [True, None]

    return [False, LS]

def programa(L):
    if not L:
        return [True, None]
    
    match L:
        case [L0]:
            R, V = linea_codigo(L0)
            return [R, V]
        
        case [PL, *RL]:
            R_pl, V_pl = linea_codigo(PL)
            if not R_pl:
                return [False, f"Error en línea: {PL}"]
            R_rl, V_rl = programa(RL)
            return [R_rl, V_rl]
    
    return [False, L]
