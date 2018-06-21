import re
from math import *
global prog
prog = {}

def load_cmd():
    f = open("p1.bas",'r') #domyślnie r
    for l in f:
        p = l.strip('\n').find(" ")
        prog[int(l[:p])]=l[p+1:].strip()

def execute(inst):
    inst = inst.lower()
    if inst.startswith("let"):
        r = re.compile(r'^let (\w+)=(.+)$')
        m = r.match(inst)
        if m:
            globals()[m.group(1)]=eval(m.group(2))    #eval z przestrzenia lokalna
        return 0
    elif inst.startswith("print"):
        print(eval(inst[6:].strip()))
        return 0
    elif inst.startswith('input'):
        globals()[inst[6:].strip()] = int(input('>'))
        return 0
    elif inst.startswith('stop'):
        return -1
    elif inst.startswith('goto'):
        et = int(inst[5:].strip())
        return et
    elif inst.startswith('if'):
        r = re.compile(r'^if +([^ ]+) +then +goto +(\d+)$')
        m = r.match(inst)
        if m:
            if eval(m.group(1)):
                return int(m.group(2))
            return 0

def run_cmd():
    global prog
    progl = [*prog] #towrzy liste z kluczy slownika LOL
    progl.sort()
    next = {}
    for i in range(len(progl)-1):
        next[progl[i]] = progl[i+1]
    next[progl[-1]] = -1
    pc = progl[0]
    while pc != -1:
        n = execute(prog[pc])
        if n == -1:
            break
        if n == 0:
            pc = next[pc]
        else:
            pc = n
def inst_cmd(cmd):
    global prog
    p = cmd.find(' ')
    et = int(cmd[:p])
    inst = cmd[p+1:].strip()
    prog[et]=inst
    return True
def new_cmd():
    global prog
    prog = {}

def list_cmd():
    global prog
    progl = [*prog]
    progl.sort()
    for e in progl:
        print(e, prog[e])
def main():
    new_cmd()
    print('BASIC ver 0.2')
    while True:
        cmd = input('>>')
        if cmd == 'new':
            new_cmd()
        elif cmd == 'run':
            run_cmd()
        elif cmd == 'list':
            list_cmd()
        elif cmd == 'load':
            load_cmd()
        elif inst_cmd(cmd):
            pass
        else:
            print('unknown command')
if  __name__ == "__main__" :
    main()
