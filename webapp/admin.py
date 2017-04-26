from django.contrib import admin

from .models import *

# Register your models here.
admin.site.register(Train)
admin.site.register(Train_Schedule)

admin.site.register(Hotel_Detail)
admin.site.register(City)