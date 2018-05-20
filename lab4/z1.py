def podz (n):
    for i in range(1, n):
        if n%i == 0:
            yield i

#for i in podz(120):
#    print(i)
#g = podz(120)
#while True:
#    print(next(g))
def prime():
    n = 2
    l = [2]
    yield 2
    while True:
        n+=1
        for i in l:
            if n%i == 0:
                break
        else:  #wykonuje się tylko jeśli pętla skończyła się normalnie  //  nie breakiem
            l.append(n)
            yield n
#for i in prime():
#    print(i)

def roz(n):
    for p in prime():
        while n % p == 0:
            n = n//p
            yield p
        if n==1:
            break
#l = [n for n in roz(120)]
#print(list(set(l)))
#k = 120
#g = (n for n in range(1,k) if k%n ==0)
#for e in g:
#    print(e)
def gen (n):
    if n == 0:
        yield ""
    else:
        for x in gen(n-1):
            yield x +"0"
            yield x +"1"
#for e in gen(5):
#    print(e)
def gen2(k,s):
    if k==0: yield ""
    else:
        for x in gen2(k-1,s):
            for y in s:
                yield
                x+y
#for e in gen2(4, "abcd"):
#    print(e)
def perm(s):
    if len(s) ==1:
        yield s
    else:
        for p in perm(s[1:]):
            for i in range(len(s)):
                yield p[:i] + [s[0]]+p[i:] # p[:i] + s[0]+p[i:]
#for e in perm(["Ala", "Ula", "Ola"]):
#    print(e)
def kmb(s, k):
    if k ==1:
        for e in s: yield e
    elif k == len(s): yield s
    else:
        for x in kmb(s[1:], k-1): yield s[0] + x
        for x in kmb(s[1:],k): yield x

#for e in kmb("abc",3):
#    print(e)
def wbzpowt(s,k):
    for kom in kmb(s,k):
        for p in perm(kom): yield p
