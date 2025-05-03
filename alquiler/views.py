from django.shortcuts import render

def index(request):
    return render(request, 'index.html')


def contacto(request):
    return render(request, 'contacto.html')

def registro(request):
    return render(request, 'registro.html')

def login(request):
    return render(request, 'login.html')

def arrendar(request):
    return render(request, 'arrendar.html')