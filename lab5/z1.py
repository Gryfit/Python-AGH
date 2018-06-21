from socket import *
from xml.dom import minidom

import time

def get_meteo():
    s = socket(AF_INET, SOCK_STREAM)
    s.connect(("meteo.ftj.agh.edu.pl",80))
    s.send(b"GET /meteo/meteo.xml\n") #10 13
    result = s.recv(1024).decode()
    s.close()
    return result

def parse_xml(done):
    t={}
    xmldoc = minidom.parseString(done)
    meteo = xmldoc.getElementsByTagName("meteo")[0]
    for d in meteo.childNodes:
        for c in d.childNodes:
            if c.nodeType == minidom.Node.ELEMENT_NODE:
                t[c.nodeName] = c.childNodes[0].nodeValue.split()[0]
    return t



buf = []
def sr(f):
    global buf
    def nowa():
        x = f()
        buf.append(x)
        if len(buf)>5:
            buf.pop(0)
        s=0.0
        for e in buf: s+=el
        s/=len(buf)
        return s
    #nowa.buf = []
    return nowa


#@sr
def get_temp():
    return float(parse_xml(get_meteo())["ta"])

f2 = sr(get_temp)

while True:
    print(parse_xml(get_meteo()))
    x = get_temp()
    y = f2
    f = open("dane","a")
    f.write("{0:4.1f} {0:4.2f}\n".format(x))
    f.close()
    time.sleep(60)
