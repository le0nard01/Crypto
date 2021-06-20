#include <iostream>
#include <vector>
#include <iomanip>
#include <string>
#include <cmath>
#include <bitset>

#define constants_size 64
#define hashpiece_size 32
#define modsize 4294967296

#define MODF3(num)      (num-(int)num) 
#define TOBIN(num)      (std::bitset<8>(num).to_string())
#define TOBIN32(num)      (std::bitset<32>(num).to_string())
#define ROTR(num,tam)   (((num >> tam) | (num << (32 - tam))) % modsize)
#define INT(string)     (stoll(string,0,2))

using namespace std;
using uint32 = unsigned long long int;


uint32 initial_round_constants[constants_size] = {2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113, 127, 131, 137, 139, 149, 151, 157, 163, 167, 173, 179, 181, 191, 193, 197, 199, 211, 223, 227, 229, 233, 239, 241, 251, 257, 263, 269, 271, 277, 281, 283, 293, 307, 311};
uint32 initial_hash_values[8] = {2, 3, 5, 7, 11, 13, 17, 19};


void ITERATION(string data, vector<string> &chunks,int size){
    for (int i = 0; i < data.size(); i+=size)
    {   
        chunks.push_back(data.substr(i,size));
    }
}

void initial_values(){
    cout.precision(32);
    uint32 x;
    x = pow(2,hashpiece_size);

    float n;
    for (size_t i = 0; i < constants_size; i++)
    {
        initial_round_constants[i] = (MODF3(pow(initial_round_constants[i],(1.0/3.0))) * x);
        //cout << "0x" << hex << fixed << (uint32)initial_round_constants[i] << ' ';
        if (i <= 7){
            initial_hash_values[i] = (MODF3(pow(initial_hash_values[i],(1.0/2.0))) * x);
            //cout << hex << fixed << (uint32)initial_hash_values[i];
        }

    }
}

string message_Schedule(string data){
    if (data.size() % 512 !=0){
        cout << "Data não é particionada em 512. Tamanho: " + data.size();
    }

    std::vector<string> chunks;
    /*for (int i = 0; i < data.size(); i+=512)
    {
        chunks.push_back(data.substr(i,i+512));
    }*/
    ITERATION(data,chunks,512);

    
    uint32 h0,h1,h2,h3,h4,h5,h6,h7;
    h0 = initial_hash_values[0];
    h1 = initial_hash_values[1];
    h2 = initial_hash_values[2];
    h3 = initial_hash_values[3];
    h4 = initial_hash_values[4];
    h5 = initial_hash_values[5];
    h6 = initial_hash_values[6];
    h7 = initial_hash_values[7];

    for (std::vector<string>::iterator it = chunks.begin() ; it != chunks.end(); ++it)
    {
        uint32 a = h0, b = h1, c = h2, d = h3, e = h4, f = h5, g = h6, h = h7;

        std::vector<string> chunk32;
        ITERATION(*it,chunk32,32);

        int const z = (64-chunk32.size());
        for (int i = 0; i < z; i++)
        {
            chunk32.push_back(string(32,'0'));
        }
        

        for (int i = 16; i < 64; i++)
        {
            uint32 s0 = ROTR(INT(chunk32[i-15]),7) ^ ROTR(INT(chunk32[i-15]),18) ^ INT(chunk32[i-15]) >> 3;
            uint32 s1 = ROTR(INT(chunk32[i-2]),17) ^ ROTR(INT(chunk32[i-2]),19) ^ INT(chunk32[i-2]) >> 10;
            chunk32[i] = TOBIN32( (INT(chunk32[i-16]) + s0 + INT(chunk32[i-7]) + s1) % modsize );
        }
        
        for (int i = 0; i < 64; i++)
        {
            uint32 s1 = ROTR(e,6) ^ ROTR(e,11) ^ ROTR(e,25);
            uint32 ch = (e & f) ^ (~e & g);
            uint32 temp1 = h+ s1 + ch + initial_round_constants[i] + INT(chunk32[i]);
            temp1 %= modsize;
            uint32 s0 = ROTR(a,2) ^ ROTR(a,13) ^ ROTR(a,22);
            uint32 maj = (a & b) ^(a & c) ^ (b & c);
            uint32 temp2 = (s0 + maj) % modsize;

            h = g;
            g = f;
            f = e;
            e = (d + temp1) % modsize;
            d = c;
            c = b;
            b = a;
            a = (temp1+temp2) % modsize;
        
        }
        
        h0 = (h0 + a) % modsize;
        h1 = (h1 + b) % modsize;
        h2 = (h2 + c) % modsize;
        h3 = (h3 + d) % modsize;
        h4 = (h4 + e) % modsize;
        h5 = (h5 + f) % modsize;
        h6 = (h6 + g) % modsize;
        h7 = (h7 + h) % modsize;
        cout << hex << h0 << ' ' << h1<< ' ' << h2 << ' '<< h3<< ' ' << h4<< ' ' << h5 << ' '<< h6<< ' ' << h7;
    }
    

}

string encode(string data){
    //std::vector<string> bits;
    string bits;
    int start_bits_len = 0;

    for (char& c : data)
    {
        string b = TOBIN((int)c);
        bits += b;
        start_bits_len += b.size();
    }
    bits.push_back('1');
    int zeros_512 = ceil((bits.size()+64)/512.0)*512 - bits.size() - 64;
    
    bits += string(zeros_512,'0');
    bits += string((64- TOBIN(start_bits_len).size()),'0') + TOBIN(start_bits_len);
    return message_Schedule(bits);
}

int main () {
    initial_values();

    cout << encode("abc");
    return 0;
}
