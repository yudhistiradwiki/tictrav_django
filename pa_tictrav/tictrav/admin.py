from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from tictrav.models import AccountCustom, TourismPlace
# Register your models here.

admin.site.register(AccountCustom)
admin.site.register(TourismPlace)