import string
import math
OP = ">&|/^"
def correct(exp):
    VAR = string.ascii_lowercase + "TF"
    brackets = 0
    for i in range(0,len(exp)-1):
        if exp[i] in VAR and exp[i+1] not in OP+")":
            return False
        if exp[i] == "~" and exp[i+1] not in VAR+"(~":
            return False
        if exp[i] == "(" and exp[i+1] not in VAR+"~"+"(":
            return False
        if exp[i] == ")" and exp[i+1] not in OP+")":
            return False
        if exp[i] in OP and exp[i+1] not in VAR+"~"+"(":
            return False
    #mozna to bylo zrobic w jednej petli ale to bez znaczenia
    brackets=0
    for e in exp:
        if e == "(":
            brackets+=1
        if e == ")":
            brackets-=1
        if brackets < 0:
            return False
    return brackets == 0

def onp(exp): #zamiana na onp wedlug algo z wikipedii
    VAR = string.ascii_lowercase + "TF"
    stack = []
    queue = ""
    operators = {'~': 4, '^': 3, '&': 2, '|': 2, '/': 2,'>': 1}
    for e in exp:
        if e in VAR:
            queue += e
        elif e in OP+"~":
            while len(stack)>0 and stack[-1] in OP+"~":
                if operators[e] -  operators[stack[-1]] <= 0 \
                    or (e == ">" and operators[e] -  operators[stack[-1]] <= 0):
                    queue += stack.pop()
                    continue
                break
            stack.append(e)
        elif e == "(":
            stack.append(e)
        elif e == ")":
            while len(stack)>0 and stack[-1] != "(":
                queue += stack.pop()
            stack.pop()
        else:
            queue += e
    while stack:
        queue += stack.pop()
    return queue

def evaluate(w, vec): #ewaluacja wyrazenia taka jak na zajeciach, dostaje wyrazenie i wektor 01011...
    operators = {
        '^': lambda x, y: int(bool(x) ^ bool(y)),
        '&': lambda x, y: int(bool(x) and bool(y)),
        '|': lambda x, y: int(bool(x) or bool(y)),
        '/': lambda x, y: int(not(bool(x) and bool(y))),
        '>': lambda x, y: int(not bool(x) or bool(y))
    }
    var = "".join(sorted(set(w) & set(string.ascii_lowercase)))
    l = list(w)
    for i in range(len(l)):
        p = var.find(l[i])
        if p >= 0: l[i] = vec[p]
    for i in range(0, len(l)):
        if l[i] == "T":
            l[i] = "1"
        if l[i] == "F":
            l[i] = "0"
    w = "".join(l)
    st = []
    for z in w:
        if z in "01": st.append(int(z))
        if z in operators:
            st.append(operators[z](st.pop(), st.pop()))
        if z == "~":
            st.append(int(not st.pop()))
    return st[0]

def ones(str):
    cc =0
    for c in str:
        if c == '1':
            cc+=1
    return cc

def makeTruthTable (exp): #tworzy liste dla ktorej wyrazenie jest prawda
    var = "".join(sorted(set(exp) & set(string.ascii_lowercase)))
    masks  = [str(bin(i)[2:].zfill(len(var))) for i in range(0, 2**len(var), 1)]
    masks = sorted(masks,key=lambda x: ones(x))
    vec = []
    for m in masks:
        if evaluate(exp, m) == 1:
            vec.append(m)
    return vec

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

def redukuj(dane): #1 poziom redukcji taki jak na zajeciach
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
    r = sorted(list(res))
    return r

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

def redukuj2(dane, orginalne): #drugi poziom redukcji w oparciu o wszystkie podzbiory w oparciu o maski bitowe
    added = set()
    t = set()
    masks  = [str(bin(i)[2:].zfill(len(orginal))) for i in range(1, 2**len(orginalne), 1)]
    masks = sorted(masks,key=lambda x: ones(x))
    for m in masks:
        if len(added) >= len(orginalne):
            t1 = sorted(list(t))
            return t1
        for d in dane:
            if pasuje(maskuj(m,orginalne),d):
                t.add(d)
                for tmp in maskuj(m,orginalne):
                    added.add(tmp)
    t1 = sorted(list(t))
    return t1

def wypisz(s, orginal): #zamiana zerdukowanych wektorow na wyrazenie
    mres =""
    used = "".join(sorted(set(orginal) & set(string.ascii_lowercase)))
    for w in s:
        res =""
        for i in range(0, len(w)): #zip(w, used):
            if w[i]=="0":
                res += "~" + used[i] + "&"
            elif w[i] =="1":
                res+= used[i] + "&"
        if len(res[:-1]) ==1:
            mres += res[:-1]+"|"
        else:
            mres +="("+res[:-1]+")|"
    return mres[:-1]

#-------------------------------------------------------


def eq(str1, str2):
    lit1 = "".join(sorted(set(str1) & set(string.ascii_lowercase)))
    lit2 = "".join(sorted(set(str2) & set(string.ascii_lowercase)))
    return lit1 == lit2

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

def shorten(s): # wyszykujemy ^/> czyli 3 etap redukcji w oparciu o porownywanie "tabelek prawdy"
#generujemy sobie tabelki prawdy dla funkcji ^/> w zalerznosci od ilosci argumentow
    if len(s)<=2:
        return ""
    v =  "".join(sorted(set(s) & set(string.ascii_lowercase)))
    tt = makeTruthTable(onp(s))
    if len(tt) == 2 ** len(v):
        return "T"
    if len(tt) == 0:
        return "F"
    nand = [str(bin(i)[2:].zfill(len(v))) for i in range(0, 2**len(v) - 1, 1)]
    if tt == nand:
        r =""
        for el in v:
            r+=el+"/"
        return r[:-1]

    if tt == nand:
        r =""
        for el in v:
            r+=el+"/"
        return r[:-1]
    #xor daje true jak jest nieparzysta liczba prawd
    allx = [str(bin(i)[2:].zfill(len(v))) for i in range(1, 2**len(v), 1)]
    xor =  list(filter(lambda x: ones(x)%2==1 ,allx))
    if tt == xor:
        r =""
        for el in v:
            r+=el+"^"
        return r[:-1]
    if len(v) == 2:
        imp = [str(bin(i)[2:].zfill(len(v))) for i in range(0, 2**len(v), 1)]
        imp.remove("10")
        if tt == imp:
            r =""
            for el in v:
                r+=el+">"
            return r[:-1]
    return s

def check(lista): #sprawdzamy wszystkie podzbiory wyrazen proboujac je skrocic i szukamy najmniejszego
    if len(lista) == 0:
        return ""
    res =""
    res_len = math.inf
    masks  = [str(bin(i)[2:].zfill(len(lista))) for i in range(1, 2**len(lista), 1)]
    for m in masks:
        tmp1 = shorten(maskuj2(m,lista))
        tmp2 = check(dopelninie(m, lista))
        if tmp1 != "":
            if(tmp2 != ""):
                tmp ="("+tmp1 +")|("+tmp2+")"
            else:
                tmp = tmp1
            if min(len(tmp), res_len):
                res = tmp
                res_len = len(res)
    return res

def bracketsrep(dane):
    c =0
    for e in dane:
        if e =="(":
            c+=1
    if c == 1 and dane[0]=="(" and dane[-1] ==")":
        return dane[1:-1]
    return dane

def order(X):
    s = ""
    for x in X:
        if x != "-":
            s +=x
        if x == "-":
            s +="0"
    return int(s,2)
    
if  __name__ == "__main__" :
    text = input("")
    expression = " ".join(text.split())
    if len(expression) == 0:
        print("ERROR")
    if not correct(expression):
        print("ERROR")
        raise SystemExit()
    #hotfix
    expression = expression.replace("~~", "")
    dane = makeTruthTable(onp(expression))
    ln =  "".join(sorted(set(expression) & set(string.ascii_lowercase)))
    if 2**len(ln) == len(dane):
        print("T")
        raise SystemExit()
    if len(dane) == 0:
        print("F")
        raise SystemExit()
    orginal = dane
    dane = redukuj(dane)
    dane = redukuj2(dane, orginal)
    dane = sorted(dane,key=lambda x: order(x),reverse=True)
    dane = wypisz(dane, expression)
    #look for NAND's True and False and XORS
    dane = check(dane.split("|"))
    dane = bracketsrep(dane)
    print(dane)

#(a&b)|(~a&~b)
#~a|~b
#~(~a|~b)
#(a|b)|(c|a|b)
#(a&~b)|(~a&b)
#(a&b&c)|(a&~b&~c)|(~a&b&~c)|(~a&~b&c)
