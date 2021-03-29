from math import ceil,sqrt
from decimal import Decimal

def modf2(x):
    z= [i for i in str(x).split('.')][::-1]
    z[0] = '0.'+z[0]
    z = [Decimal(i) for i in z]
    return z

#lista = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113, 127, 131, 137, 139, 149, 151, 157, 163, 167, 173, 179, 181, 191, 193, 197, 199, 211, 223, 227, 229, 233, 239, 241, 251, 257, 263, 269, 271, 277, 281, 283, 293, 307, 311, 313, 317, 331, 337, 347, 349, 353, 359, 367, 373, 379, 383, 389, 397, 401, 409]

def findroot_slowly_and_badly(n, k):
    n = n * (2**64)**3 
    guess = int(n ** (1/k))     
    step = (guess >> 4) + 1     
    while step != 0:
        guess_step_pow_k = (guess + step) ** k

        if guess_step_pow_k > n:
            step = step >> 1

        else:
            guess = guess + step

    return (guess & ((2**64) - 1)) 

initial_round_constants = [hex(findroot_slowly_and_badly(i,3))[2:].zfill(16) 
                        for i in [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113, 127, 131, 137, 139, 149, 151, 157, 163, 167, 173, 179, 181, 191, 193, 197, 199, 211, 223, 227, 229, 233, 239, 241, 251, 257, 263, 269, 271, 277, 281, 283, 293, 307, 311, 313, 317, 331, 337, 347, 349, 353, 359, 367, 373, 379, 383, 389, 397, 401, 409]]

initial_hash_values = [hex(int(modf2(i**Decimal(1/2))[0] * (1<<64)))[2:].zfill(16)
                        for i in [2,3,5,7,11,13,17,19]]

#print(hex(int(modf2(3**Decimal(1/2))[0] * (1<<64)))) #sqrt 
print(initial_round_constants)

#for prime in lista:
#    cubed = findroot_slowly_and_badly(prime, 3)     # cube rooting a fixed point value 3rds the bits in each part...
#                                                        # so cubed is <integer part> | <80-bit fractional part>  
#    #print(hex(cubed)[2:].zfill(16))

