"""DBMSProject URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from webapp.views import *

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^navigator/(?P<direction>[\w\-]+)/$', navigator, name='navigator'), # parameter name should be the same in the views.py
    url(r'^account_navigator/(?P<direction>[\w\-]+)/$', account_navigator, name='account_navigator'),
    url(r'^$', default),
    url(r'^get_citys/$', get_citys, name='get_citys'),
    url(r'^register/$', register, name='register'),
    url(r'^orderhotel/$', order_hotel, name='order_hotel'),
    url(r'^search_trains/$', search_trains, name='search_trains'),
    url(r'^signin/$', signin, name='signin'),
    url(r'^user_modify', user_modify, name="user_modify"),
    url(r'^search_hotel/$', search_hotel, name="search_hotel"),
    url(r'^room_hotel/(?P<hid>[\w\-]+)/$', room_hotel, name="room_hotel"),
    url(r'^pwd_modify', pwd_modify, name="pwd_modify"),
]
