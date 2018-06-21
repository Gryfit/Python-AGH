import gspread
from oauth2client.service_account import ServiceAccountCredentials
import string
import sys
import urllib.request
import json
import re
from datetime import datetime, timedelta
from functools import reduce
from validator.models import Prowadzacy, Czas, Sala

possible_data = {
    'studia': ['s1','s2','---'],
    'sem': [1,2,3,4,5,6,7],
    'pora': ['L'],
    'przedmiot': [True], #dowolna wartosc ale obowiazkowa
    'obier': ['']+list(string.ascii_uppercase),
    'typ': ['W','C','L','P'],
    'grupa': ['']+[str(i) for i in range(1, 20, 1)],
    'wym': [str(i) for i in range(1, 100, 1)], #wiecej niz 99 godzin nie przewiduje
    'prow': [False], #nie ma pewnosci czy zbior nie ulegnie zmianie w np utworzenie nowej katedry / wydzialu
    'osoba': [False], #nie obowiazkowa ale dowolne
    'miejsce': [False], #nie obowiazkowa ale dowolne
    'tyg': ['','1','2','A','B'],
    'dzien': ['','Pn','Wt','Sr','Cz','Pt'],
    'godz': [False] #ale dodamy własny filtr
}

def auth():
    scope = ['https://spreadsheets.google.com/feeds',
             'https://www.googleapis.com/auth/drive']
    credentials = ServiceAccountCredentials.from_json_keyfile_name('PythonIII-cd7f4925a852.json', scope)
    gc = gspread.authorize(credentials)
    wks = gc.open("Python3").sheet1
    return wks.get_all_records()

def validate(rows):
    global possible_data
    errorl = []
    row_num = 1
    for rw in rows:
        row_num += 1
        if rw['studia'] != '---':
            for key in possible_data:
                if key == 'godz':
                    if not (bool(re.match('\d\d:\d\d', rw[key])) or
                    bool(re.match('\d:\d\d', rw[key]))) and rw[key]!= '':
                        errorl.append("Niepoprawne dane: "+key+" Dla wiersza: " + str(row_num))
                else:
                    if str(rw[key]) not in possible_data[key]:
                        if possible_data[key][0] == True and str(rw[key]) == '':
                            errorl.append("Niekompletne dane: "+key+" Dla wiersza: " + str(row_num))
                        if possible_data[key][0] != False and possible_data[key][0] != True:
                            errorl.append("Niepoprawne dane: "+key+" Dla wiersza: " + str(row_num))
            if rw['osoba'] != '' and rw['godz'] != '':
                for p in Prowadzacy.objects.all():
                    if p.name == rw['osoba']:
                        c = Czas(pomieszczenie = rw['miejsce'],studia = rw['studia'],
                        sem = rw['sem'],tyg = rw['tyg'],
                        dzien = rw['dzien'],
                        godz = datetime.strptime(rw['godz'], '%H:%M'));
                        c.save()
                        p.save()
                        tmp = p.add(c)
                        if tmp != "":
                            errorl.append(tmp)
                        p.save()
                        break
                else:
                    c = Czas(pomieszczenie = rw['miejsce'],studia = rw['studia'],
                    sem = rw['sem'],tyg = rw['tyg'],
                    dzien = rw['dzien'],
                    godz = datetime.strptime(rw['godz'], '%H:%M'));
                    c.save()
                    pp = Prowadzacy(name = rw['osoba'])
                    pp.save()
                    tmp = pp.add(c)
                    if tmp != "":
                        errorl.append(tmp)
                    pp.save()
                if rw['miejsce'] != '':
                    for s in Sala.objects.all():
                        if s.name == rw['miejsce']:
                            c = Czas(pomieszczenie = rw['miejsce'],studia = rw['studia'],
                            sem = rw['sem'],tyg = rw['tyg'],
                            dzien = rw['dzien'],
                            godz = datetime.strptime(rw['godz'], '%H:%M'));
                            c.save()
                            s.save()
                            s.add(c)
                            s.save()
                            break
                    else:
                        ss = Sala(name = rw['miejsce'])
                        ss.save()
                        c = Czas(pomieszczenie = rw['miejsce'],studia = rw['studia'],
                        sem = rw['sem'],tyg = rw['tyg'],
                        dzien = rw['dzien'],
                        godz = datetime.strptime(rw['godz'], '%H:%M'));
                        c.save()
                        ss.save()
                        ss.add(c)
                        ss.save()
    return errorl
def find_free_room(sem,tyg): #od 8 do 19:20
    wolne_sale = []
    for s in Sala.objects.all():
        d = {
        'Name': s.name,
        'Pn': [],
        'Wt': [],
        'Sr': [],
        'Cz': [],
        'Pt': []
        }
        print(sem, tyg)
        zaj = s.list_lessons()
        zaj = sorted(zaj, key= lambda x: x.godz)
        for z in zaj:
            print(z)
            if int(z.sem)%2==sem and cmp_tyg(z.tyg, str(tyg)):
                if len(d[z.dzien])!=0 and datetime.strptime(d[z.dzien][-1], '%H:%M') - z.godz < timedelta(minutes=20):
                    d[z.dzien][-1] = (z.godz+timedelta(minutes=90)).strftime("%H:%M")
                else:
                    d[z.dzien].append(z.godz.strftime("%H:%M"))
                    d[z.dzien].append((z.godz+timedelta(minutes=90)).strftime("%H:%M"))
        wolne_sale.append(d)
    return wolne_sale

def prettyfy(ws):
    outL = []
    for s in ws:
        outD = {}
        for d in s:
            if d != 'Name':
                if len(s[d])!=0:
                    sd = list(set(s[d]))
                    sd.sort(key=lambda x: datetime.strptime(x, '%H:%M'))
                    tmp = []
                    if s[d][0] != "08:00":
                        tmp.append("08:00")
                        tmp += sd
                    else:
                        tmp += sd[1:]
                    if sd[-1] != "21:00":
                        tmp.append("21:00")
                    else:
                        tmp.remove("21:00")
                    out = ""
                    i =1;
                    for e in tmp:
                        if i%2 == 1:
                            out += e+"-"
                            i+=1
                        else:
                            out += e +"  "
                            i+=1
                    if len(tmp) != 0:
                        outD[d] = d+"    "+out[:-1]
                    outD[d] = d+"    "+out
                else:
                    outD[d] = d+"    WOLNA"
            else:
                outD['Name'] = s[d]
        outL.append(outD)
    return outL

def pretty_print_free_rooms(wolne_sale):
    for s in wolne_sale:
        print("SALA:\t"+s["Name"])
        print("--------------------------------------")
        for d in s:
            if d != 'Name':
                if len(s[d])!=0:
                    print(s[d])
                    sd = list(set(s[d]))
                    sd.sort(key=lambda x: datetime.strptime(x, '%H:%M'))
                    s[d] = sd
                    tmp = []
                    if s[d][0] != "08:00":
                        tmp.append("08:00")
                        tmp += s[d]
                    else:
                        tmp += s[d][1:]
                    if s[d][-1] != "21:00":
                        tmp.append("21:00")
                    else:
                        tmp.remove("21:00")
                    out = ""
                    i =1;
                    for e in tmp:
                        if i%2 == 1:
                            out += e+"-"
                            i+=1
                        else:
                            out += e +" "
                            i+=1
                    if len(tmp) != 0:
                        print(d+"\t"+out[:-1])
                else:
                    print(d+"\tWOLNA")
        print("--------------------------------------")
def cmp_tyg(nowe, z):
    z_ = str(z)
    n_ = str(nowe)
    if z_ == n_:
        return True
    if z_ == '' or n_ == '':
        return True
    if z_ == 'A' and n_ == '1':
        return True
    if z_ == '1' and n_ == 'A':
        return True
    if z_ == 'B' and n_ == '2':
        return True
    if z_ == '2' and n_ == 'B':
        return True
    return False
