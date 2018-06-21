from django.db import models
from datetime import datetime, timedelta

def cmp_godz(nowe, z):
    n_time_end = nowe + timedelta(minutes = 90)
    z_time_end =  z + timedelta(minutes = 90)
    return (n_time_end < z_time_end and  n_time_end > z) or (nowe < z_time_end and nowe > z) or (n_time_end == z_time_end and  nowe == z)

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

def cmp_sem(nowe, z):
    return int(nowe) == int(z)

def cmp_studia(nowe,z):
    return nowe == z

def cmp_sala(nowe,z):
    return nowe == z

def time_vlaidation(nz,z):
    return cmp_sala(nz.pomieszczenie,z.pomieszczenie) and cmp_studia(nz.studia, z.studia) and cmp_sem(nz.sem,z.sem) and cmp_tyg(nz.tyg,z.tyg) and nz.dzien == z.dzien and cmp_godz(nz.godz,z.godz)


class Czas(models.Model):
    pomieszczenie = models.CharField(max_length = 100)
    studia = models.CharField(max_length = 100)
    sem = models.CharField(max_length = 100)
    tyg = models.CharField(max_length = 100)
    dzien = models.CharField(max_length = 100)
    godz = models.DateTimeField()
    def __str__(self):
        return "Czas: sala "+str(self.pomieszczenie)+" studia: "+str(self.studia)+" sem: "+str(self.sem)+" tyg: "+str(self.tyg)+" dzien: "+str(self.dzien)+" godzina: "+self.godz.strftime("%H:%M") #rozpisać godzine
    def __repr__(self):
        return str(self)


class Prowadzacy(models.Model):
    zajecia  = models.ManyToManyField(Czas)
    name = models.CharField(max_length = 100)
    def list_lessons(self):
        return list(self.zajecia.all())
    def add(self, nz):
        for z in self.zajecia.all():
            if time_vlaidation(nz, z):
                print("Bilokacja dla prowadzacego " + str(self.name)+" "+str(nz))
                return ("Bilokacja dla prowadzacego " + str(self.name)+" "+str(nz))
        self.zajecia.add(nz)
        return ""
    def __str__(self):
        return "Prowadzacy:\t imie: "+self.name + "Zajecia:" + str(self.zajecia.all())
    def __repr__(self):
        return str(self)


class Sala(models.Model):
    zajecia = models.ManyToManyField(Czas)
    name = models.CharField(max_length = 100)
    def list_lessons(self):
        return list(self.zajecia.all())
    def add(self, nz):
            self.zajecia.add(nz)
    def __str__(self):
        return "Sala:\t nazwa: "+self.name
    def __repr__(self):
        return str(self)
# Create your models here.
