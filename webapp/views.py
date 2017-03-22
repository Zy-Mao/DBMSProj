from django.shortcuts import render, render_to_response
from django.template import Context, RequestContext
from django.http import Http404
from django.views.decorators.csrf import csrf_exempt, csrf_protect
from .models import *
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
# Create your views here.


def default(request):
    return render_to_response("main.html")


def navigator(request, direction):
    try:
        to = direction
    except ValueError:
        raise Http404
    if to == 'home':
        return render(request, "main.html")
    elif to == 'account':
        return render(request, "")
    elif to == 'travel':
        return render(request)
    elif to == 'about':
        return render(request)
    elif to == 'signin':
        return render(request, "signin.html")
    elif to == 'register':
        return render(request, "register.html")
    elif to == 'signout':
        logout(request)
        return render(request, "main.html")


@csrf_exempt
def register(request):

    try:
        User.objects.create_user(first_name=request.POST['firstname'],
                                     last_name=request.POST['lastname'],
                                     email=request.POST['email'],
                                     password=request.POST['pwd'],
                                     username=request.POST['email'],)
        u = User.objects.get(username=request.POST['email'])

        ud = User_Detail(user=u,
                         state=request.POST['state'],
                         address=request.POST['address'],
                         city=request.POST['city'],
                         zipcode=request.POST['zipcode'], )
        ud.save()

        if u.is_active:
            login(request=request, user=u)

    except Exception:
        raise Http404()
        # return render_to_response("info.html", {"isError": 1, "info_msg": "Error!"})

    return render(request, "info.html", {"isSuccess": 1, "info_msg": "Success!"})


@csrf_exempt
def signin(request):
    username = request.POST['username']
    password = request.POST['password']

    user = authenticate(username=username, password=password)

    if user is not None:
        login(request, user)
        return render(request, "info.html", {"isSuccess": 1, "info_msg": "Success!"})
    else:
        return render(request, "info.html", {"isError": 1, "info_msg": "Fail!!"})





