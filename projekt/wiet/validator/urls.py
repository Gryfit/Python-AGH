from django.urls import path

from . import views

app_name = 'validator'
urlpatterns = [
    path('', views.index, name='index'),  #just a validate button and the name of the app
    path('menu/', views.menu, name='menu'),    #validation output and menu
    path('rooms/<semester>/<week>', views.rooms, name='rooms'),   #free rooms
]
