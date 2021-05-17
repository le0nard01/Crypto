from math import ceil

def modf(x):
    z= [i for i in str(x).split('.')][::-1]
    z[0] = '0.'+z[0]
    z = [float(i) for i in z]
    return z

initial_hash_values = [hex(int(modf(i**(1/2))[0] * (1 << 32))) 
                        for i in [2,3,5,7,11,13,17,19]]

initial_round_constants = [hex(int(modf(i**(1/3))[0] * (1 << 32))) 
                        for i in [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113, 127, 131, 137, 139, 149, 151, 157, 163, 167, 173, 179, 181, 191, 193, 197, 199, 211, 223, 227, 229, 233, 239, 241, 251, 257, 263, 269, 271, 277, 281, 283, 293, 307, 311]]

def encode(string,tipo='str'): 
    def tobin(num): # transformar int em binario e preencher por 8, ou seja, tobin(10), 10 em binario é 1010, ele retornará 00001010.
        return bin(num)[2:].zfill(8)

    def rotate(num, tam):
        return ((num >> tam) | (num << (32 - tam))) % (2**32)

    def message_Schedule(data):
        if len(data) % 512 != 0:
            print(f"Data não é particionada em 512. Tamanho: {len(data)}")
            return 0

        chunks = [ data[i:i+512] for i in range(0, len(data), 512) ] # Divide os chunks de 512
        
        (h0,h1,h2,h3,h4,h5,h6,h7) = [int(i,16) for i in initial_hash_values] # cada letra é igual ao initial hash value

        for single_chunk in chunks:
            (a,b,c,d,e,f,g,h) = (h0,h1,h2,h3,h4,h5,h6,h7)
            chunk32 = [ single_chunk[i:i+32] for i in range(0, len(single_chunk), 32) ] #Dividir em chunks de 32

            for i in range(0,64-len(chunk32)): chunk32.append('0'*32) # acrescentar 0 para o total de len() = 32

            for i in range(16,64):  #parte 1 calculo sha256
                s0 = rotate(int(chunk32[i-15],2),7) ^ rotate(int(chunk32[i-15],2),18) ^ int(chunk32[i-15],2) >> 3
                s1 = rotate(int(chunk32[i-2],2),17) ^ rotate(int(chunk32[i-2],2),19) ^ int(chunk32[i-2],2) >> 10
                
                chunk32[i] = bin((int(chunk32[i-16],2) + s0 + int(chunk32[i-7],2) + s1) % (2**32))[2:]
                chunk32[i] = chunk32[i].zfill(32)

            for i in range(0,64):   #parte 2 calculo sha256
                s1 = rotate(e,6) ^ rotate(e,11) ^ rotate(e,25)
                ch = (e & f) ^ (~e & g)
                temp1 = h + s1 + ch + int(initial_round_constants[i],16) + int(chunk32[i],2)
                temp1 = temp1 % (2**32)
                s0 = rotate(a,2) ^ rotate(a,13) ^ rotate(a,22)
                maj = (a & b) ^(a & c) ^ (b & c)
                temp2 = (s0 + maj) % (2**32)
            
                h = g
                g = f 
                f = e
                e = (d + temp1) % (2**32)
                d = c
                c = b
                b = a
                a = (temp1+temp2) % (2**32)

            h0 = (h0 + a) % (2**32)
            h1 = (h1 + b) % (2**32)
            h2 = (h2 + c) % (2**32)
            h3 = (h3 + d) % (2**32)
            h4 = (h4 + e) % (2**32)
            h5 = (h5 + f) % (2**32)
            h6 = (h6 + g) % (2**32)
            h7 = (h7 + h) % (2**32)
            
        hashfinal = hex(h0),hex(h1),hex(h2),hex(h3),hex(h4),hex(h5),hex(h6),hex(h7)
        return( ''.join([(i[2:]).zfill(8) for i in hashfinal]) )

    if tipo=='str':
        bits = [ tobin(ord(x)) for x in string ] # iterar a string passada e encaminhar pra funcao tobin
    elif tipo == 'hex':
        string = string if string[0:2] != '0x' else string[2:]
        bits = [ tobin(int(string[x-2:x],16)) for x in range(2,len(string)+1,2)]

    start_bits_len = len(''.join(bits)) #tamanho da string em bit
    
    bits.append('1') # adiciona 1 no final
    bits = ''.join(bits)

    zeros_512 = ceil((len(bits)+64)/512)*512 - len(bits) - 64 # completa com '0', por multiplos de 512 em relacao ao que couber do tamanho da string, - 64.
    
    bits += zeros_512*'0' 

    bits += '0'*(64-len(tobin(start_bits_len))) + tobin(start_bits_len) #adiciona o tamanho total no final dos bits e preenche.

    return message_Schedule(bits)

print(encode('HUDSAIDASUHIJXZIJJIXZIJZKXCLSAPDQW--0-0WOOEWQOOKKKKLLKDASDKSADKSAKDSAKDKSADUI12W2UQNDWQNUJ') == 'afa01dfbd0d7fdca8bbcc98a91f297d28fbb4ac5be31f0109797156db789a52b')