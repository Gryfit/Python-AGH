import string
def lacz(s1,s2):
    res = ""
    lr =0
    for i in range(len(s1)):    #for i,j  in zip(s1,s2):
        if s1[i]==s2[i]:            #if i==j: res+=i
            res +=s1[i]             #else: res+="-"; lr+=1
        else:
            res+="-"
            lr+=1
    if lr == 1: return res
    return False
def redukuj(dane):
    res = set()
    b2 = False
    for e1 in dane:
        b1 = False
        for e2 in dane:
            wyn = lacz(e1,e2)
            if wyn:
                res.add(wyn)
                b1  = b2 = True
        if not b1: res.add(e1)
    if b2: return redukuj(res)
    return res

def wypisz(s):
    mres =""
    for w in s:
        res =""
        for i,j in zip(w, string.ascii_lowercase[:len(w)]):
            if i=="0":
                res += "~" + j + "&"
            elif i =="1":
                res+= j + "&"
        mres +="("+res[:-1]+")"+"|"
    return mres[:-1]

if  __name__ == "__main__" :
    f =open("in")
    dane = set(f.read().split()) # defaultowo split przyjmuje białe znaki i dodatkowo łączy wiele spacji #EMEJZING *o*
    print(dane)
    f.close()
    dane = redukuj(dane)
    print(dane)
    dane = wypisz(dane)
    print(dane)
