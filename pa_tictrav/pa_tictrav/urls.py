from django.contrib import admin
from django.urls import path
from tictrav import views
from tictrav.views import *
from django.contrib.auth.views import LoginView, LogoutView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/', LoginView.as_view(), name='masuk'),
    path('logout/', LogoutView.as_view(next_page='/masuk'), name='keluar'),
    path('register/', register),
    path('', index),
    path('desc/', desc),
    path('ticket/', ticket),
    path('ticketpdf/', views.ViewPDF.as_view(), name="pdf_view"),
    path('coba/', desc),
]
