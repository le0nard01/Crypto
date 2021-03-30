



def encode(string,tipo='str'):
    #constantes 
    h0 = 0x67452301
    h1 = 0xEFCDAB89
    h2 = 0x98BADCFE
    h3 = 0x10325476
    h4 = 0xC3D2E1F0

    def message_Schedule(data):
        #
    
    if tipo=='str':
        bits = [ tobin(ord(x)) for x in string ] # iterar a string passada e encaminhar pra funcao tobin

    elif tipo == 'hex':
        string = string if string[0:2] != '0x' else string[2:]
        bits = [ tobin(int(string[x-2:x],16)) for x in range(2,len(string)+1,2)]

    start_bits_len = len(''.join(bits)) #tamanho da string em bit
    
    bits.append('1') # adiciona 1 no final
    bits = ''.join(bits)
    
    zeros_512 = ceil((len(bits)+128)/1024)*1024 - len(bits) - 128 # completa com '0', por multiplos de 512 em relacao ao que couber do tamanho da string, - 64.
    
    bits += zeros_1024*'0' 

    bits += '0'*(128-len(tobin(start_bits_len))) + tobin(start_bits_len) #adiciona o tamanho total no final dos bits e preenche.

    return message_Schedule(bits)