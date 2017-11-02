import sys
import re

class BNilai:
    nilai = ''
    def __init__(self, nilai='{}>[]'):
        nilai = '('+nilai+')'
        self.nilai = nilai

    def operasi(self, op, other):
        if isinstance(other, str):
            other = '('+other+')'
            h = '('+self.nilai+op+other+')'
        elif isinstance(other, BNilai):
            h = '('+self.nilai+op+other.nilai+')'
        else:
            raise ValueError("Data Type Not Supported")
        return BNilai(h)

    def __add__(self, other):
        return self.operasi('+', other)

    def __sub__(self, other):
        return self.operasi('-', other)

    def __mul__(self, other):
        if isinstance(other, int):
            h = '('+('+'.join([self.nilai]*other))+')'
            return BNilai(h)
        return self.operasi('*', other)

    def __div__(self, other):
        return self.operasi('/', other)

    def __pow__(self, other):
        return self.operasi('**', other)

    def __lshift__(self, other):
        return self.operasi('<<', other)
    
    def __rshift__(self, other):
        return self.operasi('>>', other)

    def __lt__(self, other):
        if isinstance(other, int):
            return eval(self.nilai) < other
        elif isinstance(other, BNilai):
            return eval(self.nilai) < eval(other.nilai)
        else:
            ValueError("Data type not supported")

    def __le__(self, other):
        if isinstance(other, int):
            return eval(self.nilai) <= other
        elif isinstance(other, BNilai):
            return eval(self.nilai) <= eval(other.nilai)
        else:
            ValueError("Data type not supported")

    def __eq__(self, other):
        if isinstance(other, int):
            return eval(self.nilai) == other
        elif isinstance(other, BNilai):
            return eval(self.nilai) == eval(other.nilai)
        else:
            ValueError("Data type not supported")
    
    def __ne__(self, other):
        if isinstance(other, int):
            return eval(self.nilai) != other
        elif isinstance(other, BNilai):
            return eval(self.nilai) != eval(other.nilai)
        else:
            ValueError("Data type not supported")

    def __gt__(self, other):
        if isinstance(other, int):
            return eval(self.nilai) > other
        elif isinstance(other, BNilai):
            return eval(self.nilai) > eval(other.nilai)
        else:
            ValueError("Data type not supported")
    
    def __ge__(self, other):
        if isinstance(other, int):
            return eval(self.nilai) >= other
        elif isinstance(other, BNilai):
            return eval(self.nilai) >= eval(other.nilai)
        else:
            ValueError("Data type not supported")
    
    def __str__(self):
        return self.nilai

    def __repr__(self):
        return self.nilai

def make_bnilai(*args):
    hasil = []
    for arg in args:
        hasil += [BNilai(arg)]
    return hasil

def find_near(n, t):   # Mencari angka terdekat dari n yang mempunyai kelipatan t
    coba = [0,0]
    coba[1] = n
    coba[0] = n - (t if n%t == 0 else n%t)
    while True:
        coba[1] += 1
        if coba[1]%t == 0:
            break
    hasil = min(coba, key=lambda x:abs(x-n))
    return hasil

def avg(lst):
    return sum([ord(i) for i in lst]) / len(lst)

def generate_int(n, idx=1):
    if sys.version_info < (3,0):
        t0 = BNilai(['{}>[]','[]>[[]]','(()!=())'][idx])
        t1 = BNilai(['[[]]>=[]','[]<=[{}]', '()>[]'][idx])
    else:
        t0 = BNilai(['[]!=[]', '[]>[[]]','()==[]'][idx])
        t1 = BNilai(['[[]]>=[]', '()!=[]', '(()==())'][idx])
    t2 = t1*2
    thasil = t2
    m = 0
    if n < 0:
        m = 1
        n = abs(n)
    if n == 0:
        return t0.nilai
    elif n == 1:
        if m == 1:
            t1 = t0 - t1
        return t1.nilai
    elif n == 2:
        if m == 1:
            t2 = t0 - t2
        return t2.nilai
    elif n < 8:
        while (thasil * t2) < n:
            thasil *= t2
    else:
        while (thasil << t2) <= n:
            thasil <<= t2
    if thasil*t2 <= n:
        thasil *= t2
    sisa = n - eval(thasil.nilai)
    thasil += generate_int(sisa, idx)
    if m == 1:
        thasil = t0 - thasil
    return thasil.nilai

def make_str(s='Hello world!'):
    awal = "('c%'[::"+generate_int(-1)+"])*"+generate_int(len(s))+'%'
    isi = []
    for char in [ord(i) for i in s]:
       isi += [generate_int(char)] 
    awal += '('
    awal += ','.join(isi)
    awal += ')'
    return awal

def clean(s):
    left = []
    lr = []
    s = list(s)
    for i in range(len(s)):
        if s[i] == '(':
            left.append(i)
        elif s[i] == ')':
            n = left.pop()
            lr.append([n,i])
    for i in range(len(lr)-1):
        if lr[i][0] - lr[i+1][0] == 1 and lr[i][1] - lr[i+1][1] == -1:
            s[lr[i][0]] = ''
            s[lr[i][1]] = ''
    return ''.join(s)

def main(s):
    print(clean(make_str(s)))
    #print clean(generate_int(int(s)))

if __name__ == '__main__':
    if len(sys.argv) <= 1:
        print('Usage : {0} <str>'.format(sys.argv[0]))
        sys.exit(1)
    main(sys.argv[1])
