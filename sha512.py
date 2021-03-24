from math import ceil
from decimal import Decimal

def modf2(x):
    z= [i for i in str(x).split('.')][::-1]
    z[0] = '0.'+z[0]
    z = [Decimal(i) for i in z]
    return z

initial_hash_values = [hex(int(modf2(i**Decimal(1/3))[0] * (1 << 64))) 
                        for i in [2,3,5,7,11,13,17,19]]


x = int(modf2(2**Decimal(1/3))[0] * (1<<64))

x = modf2(2**(1/3))[0] * (2**64)

#428a2f98d728ae22     [origin]
#4794697086780616226  [origin]
#
#print(hex(int(x)))


lista = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113, 127, 131, 137, 139, 149, 151, 157, 163, 167, 173, 179, 181, 191, 193, 197, 199, 211, 223, 227, 229, 233, 239, 241, 251, 257, 263, 269, 271, 277, 281, 283, 293, 307, 311, 313, 317, 331, 337, 347, 349, 353, 359, 367, 373, 379, 383, 389, 397, 401, 409]

def findroot_slowly_and_badly(n, k):
    guess = int(n ** (1/k))     # guess is always too low
    step = (guess >> 4) + 1     # well, as long as the step size isn't so big... and at least 1
    while step != 0:
        #guess_step_cubed = (guess + step) * (guess + step) * (guess + step)
        # oops... should have used k here, instead of hard-coding the cubeness...

        guess_step_pow_k = (guess + step) ** k

        if guess_step_pow_k > n:
            # if the next step is too big, halve it smaller and try again
            step = step >> 1
        else:
            # take this step
            guess = guess + step

    return guess

#0x7137449123ef65cd

prime = 409 * (2**64)**3                          # fixed point: 2 | <240-bit fractional part>

cubed = findroot_slowly_and_badly(prime, 3)     # cube rooting a fixed point value 3rds the bits in each part...
                                                # so cubed is <integer part> | <80-bit fractional part>
fractional_bits = cubed & ((2**64) - 1)         # just get the fractional bits
print(hex(fractional_bits))
