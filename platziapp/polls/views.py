from django.shortcuts import render
from django.http import HttpResponse


def index(request):
    return HttpResponse('Estás en la página principal de Premios Platzi')


def detail(resquest, question_id):
    return HttpResponse(f"Estás viendo la pregunta número {question_id}")

def results(resquest, question_id):
    return HttpResponse(f"Estás viendo los resultados la pregunta número {question_id}")

def vote(resquest, question_id):
    return HttpResponse(f"Estás votando a la pregunta número {question_id}")
