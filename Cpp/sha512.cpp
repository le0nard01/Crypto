// array::begin example
#include <iostream>
#include <vector>
#include <cmath>
#include <iomanip>
#include <climits>

using namespace std;

unsigned long long initial_round_constants[64] = {2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113, 127, 131, 137, 139, 149, 151, 157, 163, 167, 173, 179, 181, 191, 193, 197, 199, 211, 223, 227, 229, 233, 239, 241, 251, 257, 263, 269, 271, 277, 281, 283, 293, 307, 311};
//vector< int > initial_round_constants;

long double modf2(long double num){
    return (num-(long long int)num);
}

void initial_values(){
    cout.precision(64);
    //double x = 1ULL << 32;
    cout << fixed << pow(2,(1.0/2.0)) << endl;

    unsigned long long x = ULLONG_MAX;
    float n;
    for (size_t i = 0; i < 64; i++)
    {
        initial_round_constants[i] = (modf2(pow(initial_round_constants[i],(1.0/2.0))) * x);
        cout << hex << fixed << (unsigned long long)initial_round_constants[i] << endl;
    }
    
}

int main () {
    initial_values();
    return 0;
}
