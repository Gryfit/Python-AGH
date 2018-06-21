import string
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
#    print(w)
    p = bal(w, ">")
    if p >=0:
        return onp(w[:p]) +  onp(w[p+1:]) + w[p]
    p = bal(w, "|&")
    if p >=0:
        return onp(w[:p]) +  onp(w[p+1:]) + w[p]
    if w[0]=="~":
        return w[1]+w[0]+w[2:]
    return w
def var(w):
    return "".join(sorted(set(w) & set(VAR)))

def mapuj(w,zm, val):
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
    w = mapuj(w,v,val)
    st = []
    #print(w)
    for z in w:
        if z in "01": st.append(int(z))
        elif z=="|": st.append(Or(st.pop(),st.pop()))
        elif z=="&": st.append(And(st.pop(),st.pop()))
        elif z==">": st.append(Imp(st.pop(),st.pop()))
        elif z=="~": st.append(int(not st.pop()))
    return st
def gen(n):
    for i in range(2**n):
        yield bin(i)[2:].rjust(n, "0")

if  __name__ == "__main__" :
    while True:
        w = input(">")
        if spr(w):
            v = var(w)
            lines = gen(len(v))
            for l in lines:
                print(l, value(onp(w), l))
        else:
            print("error")
