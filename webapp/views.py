from django.shortcuts import render, render_to_response
from django.http import Http404
from .models import *
# Create your views here.


def default(request):
    return render_to_response("main.html")


def navigator(request, direction):
    try:
        to = direction
    except ValueError:
        raise Http404
    if to == 'home':
        return render_to_response("main.html")
    elif to == 'account':
        return render_to_response()
    elif to == 'travel':
        return render_to_response()
    elif to == 'help':
        return render_to_response()
    elif to == 'about':
        return render_to_response()
    elif to == 'signin':
        return render_to_response()
    elif to == 'register':
        return render_to_response("register.html")


def register(request):
    t = 1
    try:
        t.save()
    except Exception:
        return render_to_response("current_time.html", {"success": "1"})

    return render_to_response("current_time.html", {"help": "1"})