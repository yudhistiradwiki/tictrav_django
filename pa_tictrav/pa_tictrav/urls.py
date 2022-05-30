from django.contrib import admin
from django.urls import path
from tictrav import views
from tictrav.views import login, register, index, ticket,desc


urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/', login),
    path('register/', register),
    path('', index),
    path('desc/', desc),
    path('ticket/', ticket),
    path('ticketpdf/', views.ViewPDF.as_view(), name="pdf_view"),
]
