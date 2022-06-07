from django.urls import path, include
from tictrav import views
from django.contrib.auth.views import LoginView, LogoutView



app_name = 'tictrav'

urlpatterns = [
    path('', views.index, name='home'),
    path('desc/<int:placeid>/', views.desc, name='deskripsi'),
    path('ticket/', views.ticket, name='ticket'),
    path('ticketpdf/', views.ViewPDF.as_view(), name="pdf_view"),
    path('login/', LoginView.as_view(), name='masuk'),
    path('logout/', LogoutView.as_view(next_page='/login'), name='keluar'),
    path('register/', views.register, name='register'),
    path('edit-profile/', views.editProfile, name='editProfile'),
    path('reservasi-tempat-wisata/<int:placeid>/', views.reservasi, name='reservasiTiket'),
]
