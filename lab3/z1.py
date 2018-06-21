import string
import re
import math
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
        return onp(w[:p]) +  onp(w[p+1:]) + w[p]
    p = bal(w, "|&")
    if p >=0:
        return onp(w[:p]) +  onp(w[p+1:]) + w[p]
    if w[0]=="~":
        return w[1]+w[0]+w[2:]
    return w
#---------------------------------------------------------
def listelements(dane):
    r = []
    tmp = ""
    i =0
    for el in dane:
        if(el != "(" and el != ")" and el != "|"):
            tmp += el
        if(el == ")"):
            r.append(tmp)
            tmp = ""
    return r
def eq(str1, str2):
    lit1 = [a for a in str1 if a in VAR]
    lit2 = [a for a in str2 if a in VAR]
    if len(lit1) != len(lit2):
        return False
    k = [True for (a,b) in zip(lit1, lit2) if a ==b]
    if len(k)==len(lit1):
        return True
    return False
def connect(listd):
    tmp = [" "]
    tmp[0]= "("+listd[0]+")"
    r = [tmp]
    for x in range(1, len(listd)):
        flag = True
        for y in range(0, len(r)):
            if(eq(listd[x], r[y][0])):
                r[y].append("("+listd[x]+")")
                flag = False
        if(flag):
            tmp = [""]
            tmp[0] = listd[x]
            r.append(tmp)
    return r

def maskuj2(mask, orginal):
    t =""
    for m,e in zip(mask,orginal):
        if m == '1':
            t += e + "|"
    return t[:-1]
def dopelninie(mask, orginal):
    t =[]
    for m,e in zip(mask,orginal):
        if m == '0':
            t.append(e)
    return t
def var(w):
    return "".join(sorted(set(w) & set(VAR)))

def mapuj3(w,zm, val):
    l = list(w)
    for i in range(len(l)):
        p = zm.find(l[i])
        if p >= 0: l[i] = val[p]
    return "".join(l)

def Or(a,b): return a or b
def And(a,b): return a and b
def Imp(a,b): return not a or b
def value(w,val):
    v = var(w)
    w = mapuj3(w,v,val)
    st = []
    for z in w:
        if z in "01": st.append(int(z))
        elif z=="|": st.append(Or(st.pop(),st.pop()))
        elif z=="&": st.append(And(st.pop(),st.pop()))
        elif z==">": st.append(Imp(st.pop(),st.pop()))
        elif z=="~": st.append(int(not st.pop()))
    return st[0]
def gen(n):
    for i in range(2**n):
        yield bin(i)[2:].rjust(n, "0")
sources = {
    '0110': "0^1",
    '01101001': "0^1^2"
}
def shorten(s):
    if len(s)<=2:
        return ""
    v = var(s)
    result =s
    r = ""
    lines = gen(len(v))
    for l in lines:
        r += str((value(onp(s), l)))
    print(r)
    flag = True
    for e in r:
        if e == "0":
            flag = False
    if flag:
        return "T"
    flag = True
    for e in r:
        if e == "1":
            flag = False
    if flag:
        return "F"
    flag = True
    for i in range(0,len(r)-1):
        if r[i] == "0":
            flag = False
    if flag and r[-1] == "0":
        variables = "".join(sorted(set(s) & set(VAR)))
        print(variables)
        r2 = ""
        for e in variables:
            r2 += e +"/"
        return r2[-1]
    if r in sources:
        result  = sources[r]
        variables = "".join(sorted(set(s) & set(VAR)))
        r2=""
        for e in result:
            if e in "0123456789":
                r2 += variables[int(e)]
            else:
                r2 += e
        result = r2
    return result
def check(lista):
    if len(lista) == 0:
        return ""
    res_len = math.inf
    masks  = [str(bin(i)[2:].zfill(len(lista))) for i in range(1, 2**len(lista), 1)]
    #print(masks)
    for m in masks:
        #print(maskuj2(m,lista),  dopelninie(m, lista))
        tmp1 = shorten(maskuj2(m,lista))
        tmp2 = check(dopelninie(m, lista))
        if tmp1 != "":
            if(tmp2 != ""):
                tmp = tmp1 +"|"+tmp2
            else:
                tmp = tmp1
            if min(len(tmp), res_len):
                res = tmp
                res_len = len(res)
    return res

#---------------------------------------------------------
if  __name__ == "__main__" :
    f =open("xor")
    dane = set(f.read().split()) # defaultowo split przyjmuje białe znaki i dodatkowo łączy wiele spacji #EMEJZING *o*
    f.close()
    orginal = dane
    dane = redukuj(dane)
    dane = redukuj2(dane, orginal)
    dane = wypisz(dane)
    #print(dane)
    k = connect(listelements(dane))
    k = check(k[0])
    print(k)
    #dane = onp(dane)
    #print(dane)
