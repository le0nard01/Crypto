from math import ceil,sqrt
from decimal import Decimal

def modf2(x):
    z= [i for i in str(x).split('.')][::-1]
    z[0] = '0.'+z[0]
    z = [Decimal(i) for i in z]
    return z

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

def encode(string, tipo='str'):
    def tobin(num): # transformar int em binario e preencher por 8, ou seja, tobin(10), 10 em binario é 1010, ele retornará 00001010.
        return bin(num)[2:].zfill(8)

    if tipo=='str':
        bits = [ tobin(ord(x)) for x in string ] # iterar a string passada e encaminhar pra funcao tobin

    elif tipo == 'hex':
        string = string if string[0:2] != '0x' else string[2:]
        bits = [ tobin(int(string[x-2:x],16)) for x in range(2,len(string)+1,2)]
    
    start_bits_len = len(''.join(bits)) #tamanho da string em bit
    
    bits.append('1') # adiciona 1 no final
    bits = ''.join(bits)
    

    #zeros_512 = ceil((len(bits)+64)/512)*512 - len(bits) - 64 # completa com '0', por multiplos de 512 em relacao ao que couber do tamanho da string, - 64.
    zeros_1024 = ceil((len(bits)+128)/1024)*1024 - len(bits) - 128 # completa com '0', por multiplos de 512 em relacao ao que couber do tamanho da string, - 64.
    bits += zeros_1024*'0' 

    bits += '0'*(128-len(tobin(start_bits_len))) + tobin(start_bits_len) #adiciona o tamanho total no final dos bits e preenche.
    print((bits))
    #return message_Schedule(bits)

encode('abc')