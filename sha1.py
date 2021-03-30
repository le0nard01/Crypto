from math import ceil

def encode(string,tipo='str'):

    def tobin(num): # transformar int em binario e preencher por 8, ou seja, tobin(10), 10 em binario é 1010, ele retornará 00001010.
        return bin(num)[2:].zfill(8)

    def leftrotate(num, tam):
        return ((num << tam) | (num >> (32 - tam))) % (2**32)

    def message_Schedule(data):
        if len(data) % 512 != 0:
            print(f"Data não é particionada em 512. Tamanho: {len(data)}")
            return 0

        chunks = [ data[i:i+512] for i in range(0, len(data), 512) ] # Divide os chunks de 512

        #constantes 
        h0 = 0x67452301
        h1 = 0xEFCDAB89
        h2 = 0x98BADCFE
        h3 = 0x10325476
        h4 = 0xC3D2E1F0

        for single_chunk in chunks:
            (a,b,c,d,e) = (h0,h1,h2,h3,h4)

            chunk32 = [ int(single_chunk[i:i+32],2) for i in range(0, len(single_chunk), 32) ] #Dividir em chunks de 32

            for i in range(0,80-len(chunk32)): chunk32.append('0'*32) # acrescentar 0 para o total de len() = 32

            for i in range(16,80):
                chunk32[i] = leftrotate(chunk32[i-3] ^ chunk32[i-8] ^ chunk32[i-14] ^ chunk32[i-16], 1)

            for i in range(80):
                if 0 <= i <= 19 :
                    f = ((b & c) | ((~b) & d)) % (2**32)
                    k = 0x5A827999
                elif 20 <= i <= 39 :
                    f = (b ^ c ^ d) % (2**32)
                    k = 0x6ED9EBA1
                elif 40 <= i <= 59 :
                    f = ((b & c) | (b & d) | (c & d) ) % (2**32)
                    k = 0x8F1BBCDC
                elif 60 <= i <= 79 :
                    f = (b ^ c ^ d) % (2**32)
                    k = 0xCA62C1D6

                b = a
                d = c
                d = e
                a = (leftrotate(a, 5) + f + e + k + chunk32[i]) % (2**32)
                c = leftrotate(b, 30)

            h0 = (h0 + a) % (2**32)
            h1 = (h1 + b) % (2**32)
            h2 = (h2 + c) % (2**32)
            h3 = (h3 + d) % (2**32)
            h4 = (h4 + e) % (2**32)

        hashfinal = hex(h0),hex(h1),hex(h2),hex(h3),hex(h4)
        return( ''.join([(i[2:]).zfill(8    ) for i in hashfinal]))

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

print(encode('abc') == 'a9993e364706816aba3e25717850c26c9cd0d89d')