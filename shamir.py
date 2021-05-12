import random

# generar un primo p (no secreto) mayor que el secreto S
PRIMO = 2**128-1

def generador_v (m, n, s):
    #Generamos aleatoriamente una lista de coeficientes (v)
    #para un polinomio de grado n-1 con la constante s
    vs=[]
    vs.append(s)
    for i in range(n - 1):
        vs.append(random.randrange(1, PRIMO))
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
    x = [i for i in range(1, m+1)]
    return tuple(polinomio(x,v))


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

    secreto = 0

    for j in range(len(partes)):
        prod = 1
        for m in range(len(partes)):
            if m != j:
                prod *= (m+1) / ((m+1) - (j+1))

        prod *= partes[j]
        secreto += prod
    return secreto

if __name__ == '__main__':


    while True:
        try:
            s = int(input('Mensaje secreto:'))
            break
        except ValueError:
            print("Secreto inadmisible, tienes que introducir un entero")


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
        print (i + 1, sol[i])
    print("El secreto era:")
    print(reconstruccion(sol))


