from django.shortcuts import render


def menu(request, *args):
    return render(request, 'menu/index.html')
