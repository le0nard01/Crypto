from math import ceil,sqrt
from decimal import Decimal

def modf(x):
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

initial_round_constants = [hex(findroot_slowly_and_badly(i,3))
                        for i in [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113, 127, 131, 137, 139, 149, 151, 157, 163, 167, 173, 179, 181, 191, 193, 197, 199, 211, 223, 227, 229, 233, 239, 241, 251, 257, 263, 269, 271, 277, 281, 283, 293, 307, 311, 313, 317, 331, 337, 347, 349, 353, 359, 367, 373, 379, 383, 389, 397, 401, 409]]

initial_hash_values = [hex(int(modf(i**Decimal(1/2))[0] * (1<<64)))
                        for i in [2,3,5,7,11,13,17,19]]

# PROCESSO PARA OBTER IV DE SHA512/t
# SHA512_IV2 = SHA512_IV ^ 0xa5a5a5a5a5a5a5a5
# Agora usa o SHA512_IV2 para encodar a mensagem 'SHA-512/t' aonde t é a truncation [normalmente 224 ou 256]
# Agora pega os novos valores de IV do resultado do encode, e utiliza eles como padrão de IV para SHA512/t expecifico.
initial_hash_values256 = [ # IV final para SHA-512/256
'0x22312194FC2BF72C', 
'0x9F555FA3C84C64C2', 
'0x2393B86B6F53B151', 
'0x963877195940EABD', 
'0x96283EE2A88EFFE3', 
'0xBE5E1E2553863992', 
'0x2B0199FC2C85B8AA', 
'0x0EB72DDC81C52CA2'] 

def encode(string, tipo='str'):
    def tobin(num): # transformar int em binario e preencher por 8, ou seja, tobin(10), 10 em binario é 1010, ele retornará 00001010.
        return bin(num)[2:].zfill(8)

    def rotate(num, tam):
        return ((num >> tam) | (num << (64 - tam))) % (2**64)

    def formathash(h): # formatar os hex, para todos hex ter 8 digitos incrementando 0's. E depois junta-los
        final = ''
        for i in h:
            i=i[2:]
            final += i.zfill(16)
        return final

    def message_Schedule(data):
        if len(data) % 1024 != 0:
            print(f"Data não é particionada em 1024. Tamanho: {len(data)}")
            return 0

        chunks = [ data[i:i+1024] for i in range(0,len(data),1024)] # Divide os chunks em 1024

        (h0,h1,h2,h3,h4,h5,h6,h7) = [int(i,16) for i in initial_hash_values]

        for single_chunk in chunks:
            (a,b,c,d,e,f,g,h) = (h0,h1,h2,h3,h4,h5,h6,h7)
            chunk64 = [ single_chunk[i:i+64] for i in range(0, len(single_chunk), 64)] # Dividir chunks em 64
            
            for i in range(0,80-len(chunk64)): chunk64.append('0'*64)

            for i in range(16,80):
                s0 = rotate(int(chunk64[i-15],2),1) ^ rotate(int(chunk64[i-15],2),8) ^ int(chunk64[i-15],2) >> 7
                s1 = rotate(int(chunk64[i-2],2),19) ^ rotate(int(chunk64[i-2],2),61) ^ int(chunk64[i-2],2) >> 6

                chunk64[i] = bin((int(chunk64[i-16],2) + s0 + int(chunk64[i-7],2) + s1) % (2**64))[2:]
                chunk64[i] = chunk64[i].zfill(64)
            
            for i in range(0,80):   #parte 2 calculo sha256
                s1 = rotate(e,14) ^ rotate(e,18) ^ rotate(e,41)
                ch = (e & f) ^ (~e & g)
                temp1 = h + s1 + ch + int(initial_round_constants[i],16) + int(chunk64[i],2)
                temp1 = temp1 % (2**64)
                s0 = rotate(a,28) ^ rotate(a,34) ^ rotate(a,39)
                maj = (a & b) ^(a & c) ^ (b & c)
                temp2 = (s0 + maj) % (2**64)
            
                h = g
                g = f 
                f = e
                e = (d + temp1) % (2**64)
                d = c
                c = b
                b = a
                a = (temp1+temp2) % (2**64)
            
            h0 = (h0 + a) % (2**64)
            h1 = (h1 + b) % (2**64)
            h2 = (h2 + c) % (2**64)
            h3 = (h3 + d) % (2**64)
            h4 = (h4 + e) % (2**64)
            h5 = (h5 + f) % (2**64)
            h6 = (h6 + g) % (2**64)
            h7 = (h7 + h) % (2**64)

        hashfinal = hex(h0),hex(h1),hex(h2),hex(h3),hex(h4),hex(h5),hex(h6),hex(h7)

        return( ''.join([(i[2:]).zfill(16) for i in hashfinal]) )

    if tipo=='str':
        bits = [ tobin(ord(x)) for x in string ] # iterar a string passada e encaminhar pra funcao tobin

    elif tipo == 'hex':
        string = string if string[0:2] != '0x' else string[2:]
        bits = [ tobin(int(string[x-2:x],16)) for x in range(2,len(string)+1,2)]
    
    start_bits_len = len(''.join(bits)) #tamanho da string em bit
    
    bits.append('1') # adiciona 1 no final
    bits = ''.join(bits)
    
    zeros_1024 = ceil((len(bits)+128)/1024)*1024 - len(bits) - 128 # completa com '0', por multiplos de 512 em relacao ao que couber do tamanho da string, - 64.
    
    bits += zeros_1024*'0' 

    bits += '0'*(128-len(tobin(start_bits_len))) + tobin(start_bits_len) #adiciona o tamanho total no final dos bits e preenche.

    return message_Schedule(bits)

#print(encode('SDJISAIJDIJSAJIDSAIJDJISAJIDSAIJDIJSAI93210D0KDSA0K0KD12K0K0D1K0D2K01K0-SAK-DK012KK0-1K-DKDKSAKDASKODSKASDJISAIJDIJSAJIDSAIJDJISAJIDSAIJDIJSAI93210D0KDSA0K0KD12K0K0D1K0D2K01K0-SAK-DK012KK0-1K-DKDKSAKDASKODSKASDJISAIJDIJSAJIDSAIJDJISAJIDSAIJDIJSAI93210D0KDSA0K0KD12K0K0D1K0D2K01K0-SAK-DK012KK0-1K-DKDKSAKDASKODSKASDJISAIJDIJSAJIDSAIJDJISAJIDSAIJDIJSAI93210D0KDSA0K0KD12K0K0D1K0D2K01K0-SAK-DK012KK0-1K-DKDKSAKDASKODSKASDJISAIJDIJSAJIDSAIJDJISAJIDSAIJDIJSAI93210D0KDSA0K0KD12K0K0D1K0D2K01K0-SAK-DK012KK0-1K-DKDKSAKDASKODSKASDJISAIJDIJSAJIDSAIJDJISAJIDSAIJDIJSAI93210D0KDSA0K0KD12K0K0D1K0D2K01K0-SAK-DK012KK0-1K-DKDKSAKDASKODSKA') == '670c73a8896cfdffa33211bfedfb13232fd4aa0e885fd3f2480ecb291d0473f2946c8ed24db9fc9979a81f05979db55f3ed134718fc7ab60ad09caf0cb077ff2')
