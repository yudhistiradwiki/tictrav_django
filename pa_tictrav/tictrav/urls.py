from django.urls import path, include
from tictrav import views
from django.contrib.auth import views as authView

from django.urls import reverse_lazy



app_name = 'tictrav'

urlpatterns = [
    path('', views.index, name='home'),
    path('desc/<int:placeid>/', views.desc, name='deskripsi'),
    path('ticket/', views.ticket, name='ticket'),
    path('ticketpdf/', views.ViewPDF.as_view(), name="pdf_view"),
    path('kota-<str:city>/', views.getWisataByKota, name='cityWisata'),
    path('reservasi-tempat-wisata/<int:placeid>/', views.reservasi, name='reservasiTiket'),

    # Akun
    path('login/', authView.LoginView.as_view(), name='masuk'),
    path('logout/', authView.LogoutView.as_view(next_page='/login'), name='keluar'),
    path('register/', views.register, name='register'),
    path('edit-profile/', views.editProfile, name='editProfile'),


    path('password_reset/', authView.PasswordResetView.as_view(template_name='account/password_reset_form.html',
        email_template_name='account/password_reset_email_template.html',
        success_url = reverse_lazy('tictrav:password_reset_done')),
        name='password_reset'),
    path('reset/<uidb64>/<token>/', authView.PasswordResetConfirmView.as_view(template_name="account/password_reset_confirm.html",
        success_url = reverse_lazy('tictrav:password_reset_complete')),
        name='password_reset_confirm'),
    path('reset/success/', authView.PasswordResetCompleteView.as_view(template_name='account/password_reset_complete.html'), 
        name='password_reset_complete'),
    path('password_reset/success/', authView.PasswordResetDoneView.as_view(template_name='account/password_reset_done.html'), 
        name='password_reset_done'),
]
