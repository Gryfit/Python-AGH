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

def ones(str):
    cc =0
    for c in str:
        if c == '1':
            cc+=1
    return cc
def maskuj(mask, orginal):
    t =[]
    for m,e in zip(mask,orginal):
        if m == '1':
            t.append(e)
    return t
def reverse(a, acc):
    if "-" not in a:
        acc.append(a)
        return acc
    i = a.find("-")
    b = a[0:i] + "1" + a[i+1:]
    reverse(b, acc)
    b = a[0:i] + "0" + a[i+1:]
    reverse(b, acc)
    return acc

def pasuje(A,b):
    B = reverse(b, [])
    for b1 in B:
        if b1 not in A:
            return False
    return True

def redukuj2(dane, orginalne):
    added = set()
    t = set()
    masks  = [str(bin(i)[2:].zfill(len(orginal))) for i in range(1, 2**len(orginalne), 1)]
    masks = sorted(masks,key=lambda x: ones(x))
    for m in masks:
        if len(added) >= len(orginalne):
            return t
        for d in dane:
            if pasuje(maskuj(m,orginalne),d):
                t.add(d)
                for tmp in maskuj(m,orginalne):
                    added.add(tmp)
    return t
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
VAR = string.ascii_lowercase
OP = "&>|"
def spr(w):
    ln = 0
    st = True
    for z in w:
        if st:
            if z in VAR:
                st=False
            elif z in ")" + OP:
                return False
        else:
            if z in OP:
                st = True
            elif z in VAR + "(":
                return False
        if z == "(":
            ln += 1
        if z == ")":
            ln -=1
        if ln <0: return False
    return not st

def bal(w, op):
    ln =0
    for i in range(len(w)-1,0,-1):
        if w[i]==")": ln -=1
        if w[i]=="(": ln +=1
        if w[i] in op and ln==0: return i
    return -1

def onp(w):
    while w[0] == "(" and w[-1] == ")" and spr(w[1:-1]) :
        w = w[1:-1]
    p = bal(w, ">")
    if p >=0:
        return w[p] + onp(w[:p]) +  onp(w[p+1:])
    p = bal(w, "|&")
    if p >=0:
        return w[p] + onp(w[:p]) +  onp(w [p+1:])
    return w

if  __name__ == "__main__" :
    f =open("xor")
    dane = set(f.read().split()) # defaultowo split przyjmuje białe znaki i dodatkowo łączy wiele spacji #EMEJZING *o*
    f.close()
    orginal = dane
    dane = redukuj(dane)
    dane = redukuj2(dane, orginal)
    dane = wypisz(dane)
    dane = onp(dane)
    print(dane)
