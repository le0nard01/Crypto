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

initial_round_constants = [hex(findroot_slowly_and_badly(i,3))
                        for i in [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113, 127, 131, 137, 139, 149, 151, 157, 163, 167, 173, 179, 181, 191, 193, 197, 199, 211, 223, 227, 229, 233, 239, 241, 251, 257, 263, 269, 271, 277, 281, 283, 293, 307, 311, 313, 317, 331, 337, 347, 349, 353, 359, 367, 373, 379, 383, 389, 397, 401, 409]]

initial_hash_values = [hex(int(modf2(i**Decimal(1/2))[0] * (1<<64)))
                        for i in [2,3,5,7,11,13,17,19]]

def encode(string, tipo='str'):
    def tobin(num): # transformar int em binario e preencher por 8, ou seja, tobin(10), 10 em binario é 1010, ele retornará 00001010.
        return bin(num)[2:].zfill(8)

    def rotate(data,tam): 
        if type(data) == int:
            data = bin(data)[2:]

        return data[len(data)-tam:]+data[0:len(data)-tam] # função de rightrotate-bitwise, mover X digitos da direita para esquerda.
    
    def shift(data,tam): return ('0'*(tam+1))+bin(int(data,2)>>tam)[2:] # função rightshift-bitwise, igual >>, só que faz a conversão para int antes.

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

        (h0,h1,h2,h3,h4,h5,h6,h7) = [int(i[2:],16) for i in initial_hash_values]

        for single_chunk in chunks:
            (a,b,c,d,e,f,g,h) = [bin(i)[2:] for i in (h0,h1,h2,h3,h4,h5,h6,h7)]
            (a,b,c,d,e,f,g,h) = [i.zfill(64) for i in (a,b,c,d,e,f,g,h)] # acrescentar 0's até ficar com len() = 64

            chunk64 = [ single_chunk[i:i+64] for i in range(0, len(single_chunk), 64)] # Dividir chunks em 64
            
            for i in range(0,80-len(chunk64)): chunk64.append('0'*64)

            for i in range(16,80):
                s0 = int(rotate(chunk64[i-15],1),2) ^ int(rotate(chunk64[i-15],8),2) ^ int(shift(chunk64[i-15],7),2) 
                s1 = int(rotate(chunk64[i-2],19),2) ^ int(rotate(chunk64[i-2],61),2) ^ int(shift(chunk64[i-2],6),2) 

                chunk64[i] = bin((int(chunk64[i-16],2) + s0 + int(chunk64[i-7],2) + s1) % (2**64))[2:]
                chunk64[i] = chunk64[i].zfill(64)
            
            for i in range(0,80):   #parte 2 calculo sha256
                s1 = int(rotate(e,14),2) ^ int(rotate(e,18),2) ^ int(rotate(e,41),2) 
                ch = (int(e,2) & int(f,2)) ^ ((~int(e,2)) & int(g,2))
                temp1 = int(h,2) + s1 + ch + int(initial_round_constants[i],16) + int(chunk64[i],2)
                temp1 = temp1 % (2**64)
                s0 = int(rotate(a,28),2) ^ int(rotate(a,34),2) ^ int(rotate(a,39),2)
                maj = (int(a,2) & int(b,2)) ^(int(a,2) & int(c,2)) ^ (int(b,2) & int(c,2))
                temp2 = (s0 + maj) % (2**64)
            
                h = (bin(int(g,2))[2:]).zfill(64)
                g = (bin(int(f,2))[2:]).zfill(64)
                f = (bin(int(e,2))[2:]).zfill(64)
                e = (bin((int(d,2) + temp1) % (2**64))[2:]).zfill(64)
                d = (bin(int(c,2))[2:]).zfill(64)
                c = (bin(int(b,2))[2:]).zfill(64)
                b = (bin(int(a,2))[2:]).zfill(64)
                a = (bin((temp1+temp2) % (2**64))[2:]).zfill(64)
            
            h0 = (h0 + int(a,2)) % (2**64)
            h1 = (h1 + int(b,2)) % (2**64)
            h2 = (h2 + int(c,2)) % (2**64)
            h3 = (h3 + int(d,2)) % (2**64)
            h4 = (h4 + int(e,2)) % (2**64)
            h5 = (h5 + int(f,2)) % (2**64)
            h6 = (h6 + int(g,2)) % (2**64)
            h7 = (h7 + int(h,2)) % (2**64)

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

print(encode('SDJISAIJDIJSAJIDSAIJDJISAJIDSAIJDIJSAI93210D0KDSA0K0KD12K0K0D1K0D2K01K0-SAK-DK012KK0-1K-DKDKSAKDASKODSKASDJISAIJDIJSAJIDSAIJDJISAJIDSAIJDIJSAI93210D0KDSA0K0KD12K0K0D1K0D2K01K0-SAK-DK012KK0-1K-DKDKSAKDASKODSKASDJISAIJDIJSAJIDSAIJDJISAJIDSAIJDIJSAI93210D0KDSA0K0KD12K0K0D1K0D2K01K0-SAK-DK012KK0-1K-DKDKSAKDASKODSKASDJISAIJDIJSAJIDSAIJDJISAJIDSAIJDIJSAI93210D0KDSA0K0KD12K0K0D1K0D2K01K0-SAK-DK012KK0-1K-DKDKSAKDASKODSKASDJISAIJDIJSAJIDSAIJDJISAJIDSAIJDIJSAI93210D0KDSA0K0KD12K0K0D1K0D2K01K0-SAK-DK012KK0-1K-DKDKSAKDASKODSKASDJISAIJDIJSAJIDSAIJDJISAJIDSAIJDIJSAI93210D0KDSA0K0KD12K0K0D1K0D2K01K0-SAK-DK012KK0-1K-DKDKSAKDASKODSKA') == '670c73a8896cfdffa33211bfedfb13232fd4aa0e885fd3f2480ecb291d0473f2946c8ed24db9fc9979a81f05979db55f3ed134718fc7ab60ad09caf0cb077ff2')
