from django.shortcuts import render, render_to_response
from django.template import Context, RequestContext
from django.http import Http404
from django.views.decorators.csrf import csrf_exempt, csrf_protect
from .models import *
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.db.models import Q
import time
from datetime import datetime
from datetime import timedelta
from django.utils import timezone
from django.utils.dateparse import parse_date
from django.db import connection
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
import json
# Create your views here.


def default(request):
    city_list = City.objects.all()
    return render(request, "main.html", {"city_list": city_list})

def navigator(request, direction):
    try:
        to = direction
    except ValueError:
        raise Http404
    if to == 'home':
        city_list = City.objects.all()
        return render(request, "main.html", {"city_list": city_list})
    elif to == 'account':
        return render(request, "account_info.html")
    elif to == 'travel':
        city_list = City.objects.all()
        return render(request, "main.html", {"city_list": city_list})
    elif to == 'hotel':
        return render(request, "search_hotel.html")
    elif to == 'about':
        return render(request)
    elif to == 'signin':
        return render(request, "signin.html")
    elif to == 'register':
        return render(request, "register.html")
    elif to == 'signout':
        logout(request)
        city_list = City.objects.all()
        return render(request, "main.html", {"city_list": city_list})


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
        return render(request, "info.html",
                      {"isError": 1, "info_msg": "Account is NOT exist or Password is NOT correct."})
    return render(request, "info.html", {"isSuccess": 1, "info_msg": "Success!"})


@csrf_exempt
def signin(request):
    username = request.POST['username']
    password = request.POST['password']

    user = authenticate(username=username, password=password)

    if user is not None:
        login(request, user)
        return render(request, "info.html", {"isSuccess": 1, "info_msg": "Sign in Successfully"})
    else:
        return render(request, "signin.html", {"isError": 1, "info_msg": "Account is NOT exist or Password is NOT correct."})


def account_navigator(request, direction):
    try:
        to = direction
        u = request.user
        ud = User_Detail.objects.get(user_id=u.id)
    except ValueError:
        raise render(request, "info.html", {"isError": 1, "info_msg": "Error"})
    if to == 'info':
        return render(request, "account_info.html", {"show_id": 1, "state": ud.state, "zipcode": ud.zipcode, "city": ud.city, "address": ud.address})
    elif to == 'infomodify':

        return render(request, "account_info.html", {"show_id": 2, "ud": ud})
    elif to == 'pwdmodify':
        return render(request, "account_info.html", {"show_id": 3})
    elif to == 'order':
        orders = Order.objects.filter(user_id_id=u.id)
        return render(request, "order_list.html", {"orders": orders})


def dictfetchall(cursor):
    "Return all rows from a cursor as a dict"
    columns = [col[0] for col in cursor.description]
    return [
        dict(zip(columns, row))
        for row in cursor.fetchall()
    ]


@login_required(login_url='/navigator/signin/')
def user_modify(request):
    u = request.user


@csrf_exempt
def pwd_modify(request):
    try:
        old_password = request.POST['cpwd']
        new_password = request.POST['npwd']

        user = authenticate(username=request.user.email, password=old_password)
        u = User.objects.get(username=request.user.email)
    except ValueError:
        raise render(request, "info.html", {"isError": 1, "info_msg": "Error"})
    if user is not None:
        u.set_password(new_password)
        u.save()
        logout(request)
        return render(request, "info.html", {"isSuccess": 1, "info_msg": "Password modify Successfully. Please signin again."})
    else:
        return render(request, "account_info.html", {"show_id": 3, "error_info": "Your password is NOT correct."})


@csrf_exempt
def get_citys(request):
    # if request.is_ajax():
    q = request.GET.get('term', '')
    citys = City.objects.filter(city__contains=q)[:20]
    results = []
    for city in citys:
        city_json = {}
        city_json['id'] = city.cid
        city_json['label'] = city.city + ', ' + city.state
        city_json['value'] = city.city
        results.append(city_json)
    data = json.dumps(results)
    # else:
    #    data = 'fail'
    mimetype = 'application/json'
    return HttpResponse(data, mimetype)


@csrf_exempt
def search_hotel(request):
    try:
        hcity = request.POST['scity']

        htype = request.POST['htype']
        print(hcity, htype)
    except Exception:
        hcity = request.GET.get('scity')

        htype = request.GET.get('htype')

    if hcity == '':
        hotels = Hotel_Detail.objects.all()
    else:
        hotels = Hotel_Detail.objects.filter(city__contains=hcity)
        # hotels = Hotel_Detail.objects.filter(city__contains=hcity)

    if htype != 'ALL':
        hotels = hotels.filter(type=htype)

    paginator = Paginator(hotels, 10)

    page = request.GET.get('page')
    try:
        hotels_list = paginator.page(page)
    except PageNotAnInteger:
        hotels_list = paginator.page(1)
    except EmptyPage:
        hotels_list = paginator.page(paginator.num_pages)
    # hotels = Hotel_Detail.objects.filter(type__exact=htype)
    return render(request, "hotel_list.html", {"hotels": hotels_list, "a":htype, "b":hcity})


def room_hotel(request, hid):
    hotel = Hotel_Detail.objects.get(hotel_id=hid)

    hotel_room = Hotel_Room.objects.filter(hotel=hotel)

    return render(request, "room_hotel.html", {"hotel_room": hotel_room, "hotel": hotel})


@csrf_exempt
def order_hotel(request):
    try:
        hid = request.POST['hid']
        rid = request.POST['choice']
        user = request.user
        checkin = request.POST['indate']
        checkout = request.POST['outdate']
    except Exception:
        raise render(request, "info.html", {"isError": 1, "info_msg": "Error"})
    checkin = datetime.strptime(checkin, '%Y-%m-%d')
    checkout = datetime.strptime(checkout, '%Y-%m-%d')

    days = checkout - checkin

    for i in range(0, days.days):
        ddate = checkin + timedelta(days=i)
        ddate = ddate.strftime('%Y-%m-%d')
        if not isAvaliableRoom(rid, ddate):
            return render(request, "room_hotel.html", {"order_status": 0})

    ohotel = Hotel_Detail.objects.get(hotel_id=hid)
    oroom = Hotel_Room.objects.get(room_no=rid)

    return render(request, "confirm_hotel_order.html",
                  {"order_status": 1, "ohotel": ohotel, "oroom": oroom,
                   "checkin": checkin.strftime('%Y-%m-%d'), "checkout": checkout.strftime('%Y-%m-%d'),
                   "period": days.days})


def hotelOrderDetail(request, oid):
    order = Order.objects.get(id=oid)
    hotel_orders = Hotel_Order.objects.filter(order_id=order.id)

    room = Hotel_Room.objects.get(room_no=hotel_orders[0].hotel_room_id)

    hotel = Hotel_Detail.objects.get(hotel_id=room.hotel_id)

    return render(request, "detail_hotel_order.html", {"oroom": room, "order": order, "ohotel": hotel})


# date should be yyyy-mm-dd
# rid: room_id
def isAvaliableRoom(rid, checkin):
    with connection.cursor() as cursor:
        cursor.execute("select 1 from webapp_hotel_order t where t.indate = to_date(%s, \'yyyy-mm-dd\') and t.hotel_room_id = %s", [checkin, rid])
        row = cursor.fetchone()
    if row == None:
        return True
    else:
        return False

@csrf_exempt
def comfirm_hotel_order(request):
    try:
        hid = request.POST['hid']
        rid = request.POST['choice']
        user = request.user
        checkin = request.POST['indate']
        checkout = request.POST['outdate']
        total = request.POST['order_summary']
    except Exception:
        raise render(request, "info.html", {"isError": 1, "info_msg": "Error"})
    checkin = datetime.strptime(checkin, '%Y-%m-%d')
    checkout = datetime.strptime(checkout, '%Y-%m-%d')

    days = checkout - checkin

    for i in range(0, days.days):
        ddate = checkin + timedelta(days=i)
        ddate = ddate.strftime('%Y-%m-%d')
        if not isAvaliableRoom(rid, ddate):
            return render(request, "info.html", {"isError": 1, "info_msg": "Error"})

    order_date = time.strftime('%Y-%m-%d')
    # u = User_Detail.objects.get(user_id=user.id)
    order = Order(order_type='H', total_amount=total, user_id_id=user.id, order_date=order_date)
    order.save()

    for i in range(0, days.days):
        ddate = checkin + timedelta(days=i)
        ddate = ddate.strftime('%Y-%m-%d')
        ho = Hotel_Order(hotel_room_id=rid, indate=ddate, user_id=user.id, order_id=order.id)
        ho.save()
    return render(request, "info.html", {"isSuccess": 1, "info_msg": "Order Successfully!"})


@csrf_exempt
def search_trains(request):
    result_list = []
    departure_city_name = City.objects.filter(cid=request.POST.get('dp', False)).first().city
    arrival_city_name = City.objects.filter(cid=request.POST.get('ar', False)).first().city
    date = request.POST.get('dd', False)
    print(date.split('-')[0], date.split('-')[1], date.split('-')[2])
    for train in Train.objects.all():
        try:
            train_schedule_list = train.train_schedule_set
            departure_train_schedule_list = train_schedule_list.filter(arrival_city=departure_city_name)
            arrival_train_schedule_list = train_schedule_list.filter(arrival_city=arrival_city_name)
        except ValueError:
            raise render(request, "info.html", {"isError": 1, "info_msg": "Error"})
        print(departure_train_schedule_list.count())
        print(arrival_train_schedule_list.count())
        if departure_train_schedule_list.count() > 0 and arrival_train_schedule_list.count() > 0 \
                and arrival_train_schedule_list.first().arrival_time > departure_train_schedule_list.first().arrival_time:
            ticket_remain = train.ticket_amount - \
                            Train_Sub_Order.objects.filter(departure_city__train=train, date__year=date.split('-')[0],
                                                           date__month=date.split('-')[1], date__day=date.split('-')[2]).count()
            if ticket_remain > 0:
                train_info_url = str(departure_train_schedule_list.first().id) + "_" + str(arrival_train_schedule_list.first().id) + "_" + \
                    date.split('-')[0] + "_" + date.split('-')[1] + "_" + date.split('-')[2]
                result_list.append((train_info_url, departure_train_schedule_list.first(), arrival_train_schedule_list.first(),
                                    arrival_train_schedule_list.first().price - departure_train_schedule_list.first().price,
                                    ticket_remain))

    return render(request, "train_list.html", {"result_list": result_list})

@csrf_exempt
def train_info(request, train_info_url):
    departure_train_schedule_id = train_info_url.split('_')[0]
    arrival_train_schedule_id = train_info_url.split('_')[1]
    train_schedule_year = train_info_url.split('_')[2]
    train_schedule_month = train_info_url.split('_')[3]
    train_schedule_day = train_info_url.split('_')[4]
    departure_train_schedule_info = Train_Schedule.objects.filter(id=departure_train_schedule_id).first()
    arrival_train_schedule_info = Train_Schedule.objects.filter(id=arrival_train_schedule_id).first()
    train_time_table_set = departure_train_schedule_info.train.train_schedule_set.all().order_by('price')

    return render(request, "train_info.html", {"train" : departure_train_schedule_info.train,
                                               "train_time_table_set": train_time_table_set,
                                               "departure_train_schedule" : departure_train_schedule_info,
                                               "arrival_train_schedule" : arrival_train_schedule_info,
                                               "train_schedule_date" : train_schedule_year + "-" + \
                                                                       train_schedule_month + "-" + train_schedule_day})

@csrf_exempt
def order_train(request):
    train_sub_order_list = []
    user_info = request.user
    ticket_order_amount = request.POST.get("ticket_order_amount", False)
    departure_train_schedule_info = Train_Schedule.objects.filter(id=request.POST.get("dtid", False)).first()
    arrival_train_schedule_info = Train_Schedule.objects.filter(id=request.POST.get("atid", False)).first()
    train_schedule_date = request.POST.get("train_schedule_date", False)
    # try:
    user_detail_info = User_Detail.objects.filter(user=user_info).first()
    if user_detail_info is None:
        # not request.user.is_authenticatedis or
        return render(request, "info.html", {"isError": 1, "info_msg": "Could not find user, please login."})
    # except Exception:
    #     return render(request, "info.html", {"isError": 1, "info_msg": "Could not find user, please login."})
    train_order_info = Train_Order(user=user_detail_info, transaction_date=timezone.now())
    train_order_info.save()
    for i in range(int(ticket_order_amount)):
        train_sub_order = Train_Sub_Order(date=parse_date(train_schedule_date),
                                          departure_city=departure_train_schedule_info,
                                          arrival_city=arrival_train_schedule_info)
        train_sub_order_list.append((train_sub_order, arrival_train_schedule_info.price - departure_train_schedule_info.price))
        train_sub_order.save()

    # print(arrival_train_schedule_info.price - departure_train_schedule_info.price)

    return render(request, "confirm_train_order.html", {"train_order_info" : train_order_info,
                                                        "train_sub_order_list" : train_sub_order_list,
                                                        "single_price" : arrival_train_schedule_info.price
                                                                         - departure_train_schedule_info.price,
                                                        "ticket_order_amount" : ticket_order_amount,
                                                        "total_price" : float(ticket_order_amount)
                                                                        * (arrival_train_schedule_info.price
                                                                           - departure_train_schedule_info.price)})