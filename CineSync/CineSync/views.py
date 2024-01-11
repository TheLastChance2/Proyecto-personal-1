from django.shortcuts import render

def mostrar_colores(request):
    return render(request, 'colores.html')

def mostrar_base(request):
    return render(request, 'base.html')