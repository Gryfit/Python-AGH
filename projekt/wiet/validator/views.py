from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse

from validator.models import Prowadzacy, Czas, Sala
from validator.val import validate, auth, find_free_room, pretty_print_free_rooms, prettyfy

# Create your views here.


#zamienic pomysl z wyjatkami na stringi i wyswietlac je ladnie w liscie
errl = []
def index(request):
    return render(request, 'validator/index.html',)

def menu(request):
    global errl
    if request.method == 'GET':
        if not Prowadzacy.objects.all().exists():
            rows_list = auth()
            errl =  validate(rows_list)
            if errl:
                return render(request, 'validator/menu.html', {
                'validation_output': "Failed",
                'error_list': errl,
                'error': 1
                })
            else:
                return render(request, 'validator/menu.html',{
                'validation_output': "OK",
                'error_list': [],
                'error': 0
                })
        else:
            if not errl:
                return render(request, 'validator/menu.html',{
                'validation_output': "OK",
                'error_list': [],
                'error': 0
                })
            else:
                return render(request, 'validator/menu.html',{
                'validation_output': "Failed",
                'error_list': errl,
                'error': 1
                })
    else:
        sem = request.POST.get('sem_f', 'p')
        tyg = request.POST.get('tyg_f','A')
        if (sem == 'p' or sem == 'np') and (tyg == "A" or tyg == "B"):
            if sem == 'p':
                s = 0
            if sem == 'np':
                s = 1
            return rooms(request,semester = s, week = tyg)
        else:
            return render(request, 'validator/menu.html',{
            'validation_output': 'Unknown parameters',
            'error_list': [],
            'error': 1
            })
def rooms(request, semester, week):
    rs = find_free_room(semester,week)
    prs = prettyfy(rs)
    pretty_print_free_rooms(rs)
    return render(request,'validator/room.html',{'list': prs})
