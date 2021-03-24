from math import ceil,modf
from decimal import Decimal

def modf2(x):
    z= [i for i in str(x).split('.')][::-1]
    z[0] = '0.'+z[0]
    z = [float(i) for i in z]
    return z

#x = modf2(2**Decimal(1/3))[0]

#29,67,127,131,223

x1 = modf(29**(1/3))
x2 = modf2(29**(1/3))
print(x1,x2)