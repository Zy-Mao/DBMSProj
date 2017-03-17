from django.shortcuts import render, render_to_response
from django.http import Http404

# Create your views here.


def default(request):
    return render_to_response("base.html")

def navigator(request, direction):
    try:
        to = str(direction)
    except ValueError:
        raise Http404
    if to == 'home':
        return render_to_response()
    elif to == 'account':
        return render_to_response()
    elif to == 'travel':
        return render_to_response()
    elif to == 'help':
        return render_to_response()
    elif to == 'about':
        return render_to_response()


