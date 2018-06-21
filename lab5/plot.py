from pylab import *

f = open("dane", "r")
lista = []
for i in f:
    lista.append(i.split()[0])
f.close()
plot(lista)
savefig("wykres.png")
