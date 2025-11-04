def RT(M,NR,RR): 
    RR.append([F[:] for F in M]) 
    if NR == 0:
        return RR
    n = len(M)
    B = [] 

    B.extend(M[0])

    for i in range(1, n - 1):
        B.append(M[i][n - 1])
    if n > 1:
        B.extend(M[n - 1][::-1])
    for i in range(n - 2, 0, -1):
        B.append(M[i][0])

    B = B[-3:] + B[:-3]

    i = 0 

    for j in range(3):
        M[0][j] = B[i]
        i += 1
    for i in range(1, 2):
        M[i][2] = B[i]
        i += 1

    for j in range(2, -1, -1):
        M[2][j] = B[i]
        i += 1

    for i in range(1, 2):
        M[i][0] = B[i]
        i += 1

    return RT(M, NR - 1,RR)

M = [['*'] * 3 for _ in range(3)]
M[0][0] = 'Cb0'
M[0][2] = 'Cb1'
M[2][0] = 'Cn0'
M[2][2] = 'Cn1'

RO = 4 
HR = RT(M,RO,[]) 

for S, E in enumerate(HR): 
    print(f"Rotación {S}:")
    print("*-----------------*")
    for F in E:
        print("| " + " | ".join(f"{C:>3}" for C in F) + " |") 
    print("*-----------------*")
    print()
