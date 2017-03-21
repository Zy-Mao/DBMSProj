from django.shortcuts import render, render_to_response
from django.http import Http404
from django.views.decorators.csrf import csrf_exempt
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

@csrf_exempt
def register(request):
    t = User(email=request.POST['email'],
             firstname=request.POST['firstname'],
             lastname=request.POST['lastname'],
             password=request.POST['pwd'],
             gender=request.POST['gender'],
             state=request.POST['state'],
             city=request.POST['city'],
             address=request.POST['address'],
             zipcode=request.POST['zipcode'],)
    try:
        t.save()
        request.user.is_authenticated
    except Exception:
        raise Http404()
        # return render_to_response("info.html", {"isError": 1, "info_msg": "Error!"})

    return render_to_response("info.html", {"isSuccess": 1, "info_msg": "Success!"})