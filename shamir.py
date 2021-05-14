import random
from decimal import Decimal

# generar un primo p (no secreto) mayor que el secreto S
PRIMO = 2**128-1

def generador_v (m, n, s):
    #Generamos aleatoriamente una lista de coeficientes (v)
    #para un polinomio de grado n-1 con la constante s
    vs=[]
    vs.append(s)
    for i in range(n - 1):
        vs.append(random.randrange(1, m))
    return vs

def comparticiones(s, n, m):
    #Polinomio
    """Polinomio de grado n-1:
       F(v) = (xn-1vn-1 + xn-2vn-2 + ... + x2v2 + x1v1 + S) modulo p.
       """
    # Dando valores a v con v = 1...m se obtienen m ecuaciones,
    # de las cuales sólo n son independientes, de modo que cualesquiera
    # n bastan para resolver el sistema de ecuaciones.
    v = generador_v(m, n, s)
    #v=[1234, 166, 94]
    x = [i for i in range(1, m+1)]
    particiones=polinomio(x, v)
    resultado=[]
    for i in range(len(x)):
        resultado.append((x[i], particiones[i]))
    return resultado


def polinomio (x, v):
    pol=[]
    suma=0
    for i in range(len(x)):
        for j in range(len(v)):
            suma+=v[j]*(x[i]**(j))
        pol.append(suma%PRIMO)
        suma=0
    return pol

def reconstruccion(partes):
    #Para reconstruir el secreto basta con juntar n ecuaciones a partir
    #de los datos de n custodios, resolviendo el sistema y obteniendo S.
    #Si no se pueden juntar n ecuaciones, el sistema tiene infinitas soluciones
    #  y por tanto se tiene información cero. El sistema puede resolverse por
    #  el método de Lagrange.

    sumatorio = 0

    for j, secreto_de_j in enumerate(partes):
        xj, yj = secreto_de_j
        productorio = Decimal(1)

        for m, secreto_de_m in enumerate(partes):
            xm, ym = secreto_de_m
            if m != j:
                productorio *= Decimal(Decimal(xm) / (xm - xj))

        productorio *= yj
        sumatorio += Decimal(productorio)

    return int(round(Decimal(sumatorio), 0))

def ascii_to_char(asci, tam_asci):
    secreto=''
    i=0
    j=0
    while i<len(asci):
        tam_caracter=tam_asci[j]
        if tam_caracter == 2:
            secreto += str(chr(int(asci[i] + asci[i + 1])))
            i+=2
        else:
            secreto += str(chr(int(asci[i] + asci[i + 1] + asci[i+2])))
            i+=3
        j+=1
    return secreto
if __name__ == '__main__':

    secreto=input('Dime tu secreto:')
    s=''
    tam_del_ascii=[]

    for i in range(len(secreto)):
        s+=str(ord(secreto[i]))
        tam_del_ascii.append(len(str(ord(secreto[i]))))
    s=int(s)
    print(s)

    while True:
        try:
            m=int(input(('m:')))
            break
        except ValueError:
            print("Tienes que introducir un entero")

    while True:
        try:
            n = int(input('n: '))
            if (n>m): raise ValueError
            break
        except ValueError:
            print("Tienes que introducir un entero menor que m")

    sol = comparticiones(s, n, m)

    print('Las reparticiones quedan:')
    for i in range (len(sol)):
        print(sol[i][0], sol[i][1])

    recon=str(reconstruccion(sol))

    print('secreto en ascii', recon)
    print('Tu secreto es:', ascii_to_char(recon, tam_del_ascii))
