from ctypes.wintypes import INT
from select import select
from django.shortcuts import render, redirect
from django.http.response import HttpResponse
from io import BytesIO
from django.views import View
from django.template.loader import get_template
from xhtml2pdf import pisa
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.conf import settings

# Exception
from django.core.exceptions import PermissionDenied


# Model DB tictrav
from tictrav import models, forms

# from django.db.models import Count

# Pemodelan AI
from model_development import model as md


# Random generator dan pattern
import re
import random
import datetime

# Pesan
from django.contrib import messages


# Create your views here.
model_statictis_item = None
model_predict = None

"""
    Account
"""
# Login
# def login(request):
#     if(request.method == 'POST'):
#         email=request.POST['email']
#         password=request.POST['password']
#         user = authenticate(request, email=email, password=password)
#         if not user:
#             return redirect("/")
#         login(request, user)
#     return redirect("/")

# Register
def register(request):
     if request.method=='POST':
        _, fullname, age, email, password = request.POST.values()
        
        """
            Pengecekan duplikasi email
        """
        try:
            user = models.AccountCustom.objects.get(email=email)
        except:
            user = models.AccountCustom.objects.create_user(email,password,fullname,age)
            user.save()
        else:
            messages.add_message(request, messages.ERROR, 'Duplikasi akun ditemukan. Gunakan akun yang berbeda')
            return redirect("/login")    
     return redirect("/login")

# Logout
def logout(request):
    logout(request)
    return redirect("/")

#Home
def index(request):
    global model_predict
    recommend = None
    tourism = models.TourismPlace.objects.all()
    data = {
        'place_id':[i.place_id for i in tourism],
        'place_name':[i.place_name for i in tourism],
        'category':[i.category for i in tourism],
    }
    if request.user.is_authenticated:
        personal = [i.category for i in models.personalization.objects.filter(user=request.user)]

        if model_predict == None:
            model_predict = md.Model('ModelUserAgeTourismConcate(Dipake)',data)
        
        recommend = model_predict.predict(request.user.id,request.user.age)
        if personal:
            recommend = models.TourismPlace.objects.filter(pk__in=recommend, category__in=personal)
        else:
            recommend = models.TourismPlace.objects.filter(pk__in=recommend)


    # tourism = models.TourismPlace.objects.values('city').annotate(jum_city=Count('city')).order_by()
    return render(request, 'home.html',{'tourism': tourism,'recommend':recommend})

def desc(request, placeid):
    global model_statictis_item
    tourism = models.TourismPlace.objects.get(place_id=placeid)

    comments = models.Reservation.objects.select_related().filter(place_id=placeid)

    # Inisialisasi model hanya sekali
    if model_statictis_item == None:
        reservation = models.Reservation.objects.values_list('user','place','place_ratings')
        # 0 user 1 item
        model_statictis_item = md.colaborative_calculation_statistik(reservation,"place",1)

    # Penghapusan karakter place_ hasil get_dummies
    recommend = model_statictis_item.itemRecommendedByItem(tourism.place_id, 5)
    recommend = models.TourismPlace.objects.filter(pk__in=recommend)

    return render(request, "desc.html", {'data':tourism, 'recommend':recommend, 'comments':comments})


@login_required(login_url=settings.LOGIN_URL)
def editProfile(request):
    if request.method=='POST':
        _, email, fullname, age, location, password = request.POST.values()
        user_form = forms.EditUserForm(request.POST, instance=request.user)
        if user_form.is_valid():
            user_form.save()
        return redirect('/edit-profile')
    try:
        user_form = forms.EditUserForm(instance=request.user)
    except:
        return redirect('/login')

    return render(request, "account/editprofile.html",{'user_form':user_form})


@login_required(login_url=settings.LOGIN_URL)
def personalize(request):
    personal = [i.category for i in models.personalization.objects.filter(user=request.user)]


    if request.method=='POST':
        userCategory = []
        for i in request.POST.getlist('kategori'):
            userCategory.append(i)

        for i in personal:
            if(i not in userCategory):
                models.personalization.objects.filter(user=request.user,category=i).delete()

        for i in userCategory:
            if(i not in personal):
                personalDB = models.personalization(user=request.user,category=i)
                personalDB.save()




        return redirect('/personalization')

    category = models.TourismPlace.objects.all()
    
    return render(request, "account/personalisasi.html",{'categories':category,'personal':personal})

def getWisataByKota(request, city):
    tourism = models.TourismPlace.objects.filter(city=city)
    return render(request, "kotawisata.html",{'tourism':tourism,'city':city}) 

"""
    Pemesanan reservasi
"""
# Reservasi
@login_required(login_url=settings.LOGIN_URL)
def reservasi(request,placeid):
    tourism = models.TourismPlace.objects.get(place_id=placeid)
    if request.method == 'POST':
        _, fullname, email, phone, location, due_date = request.POST.values()
        
        # Update akun bila ada perubahan
        account = models.AccountCustom.objects.get(id=request.user.id)
        account.full_name = fullname
        account.location = location
        account.email = email
        account.phone_number = phone
        account.save()
        
        reservasi_user = models.Reservation.objects.create(user = request.user , place = tourism, due_date = request.POST['due_date']) 
        reservasi_user.save()

        return redirect(f'/ticket/')


    reservasi_form =  forms.ReservationForm(instance=request.user)
    return render(request, "pemesanan.html",{'reservation':reservasi_form,'tourism':tourism})

@login_required(login_url=settings.LOGIN_URL)
def ratePlace(request, placeid):
    if request.method == 'POST':
        reservation = models.Reservation.objects.filter(user_id=request.user.id, place_id=placeid)
        if not reservation:
            messages.add_message(request, messages.ERROR, 'Pengguna belum melakukan reservasi')
        else:
            for i, reserve in enumerate(reservation):
                if((len(reservation)-i)==1):
                    reserve.place_ratings = request.POST['stars']
                    reserve.comments = request.POST['comments']
                    reserve.save()
        return redirect(f'/desc/{placeid}')
    raise PermissionDenied



#Ticket
def render_pdf(template_src, context_dict={}):
    template = get_template(template_src)
    html = template.render(context_dict)
    result = BytesIO()
    pdf = pisa.pisaDocument(BytesIO(html.encode("ISO-8859-1")), result)
    if not pdf.err:
        return HttpResponse(result.getvalue(), content_type='application/pdf')
    return None



class ViewPDF(View):
    def get(self, request, *args, **kwargs):
        pdf = render_pdf('tickets/ticket.html', data)
        return HttpResponse(pdf, content_type='application/pdf')


def ticket(request):
    reservation = models.Reservation.objects.select_related().filter(user_id=request.user.id)
    for i, reserve in enumerate(reservation):
        if((len(reservation)-i)==1):
            data = {
                "nama" : request.user.full_name,
                "wisata" :reserve.place.place_name,
                "city" : reserve.place.city,
                "reservasi_id":reserve.place, 
                "time" : reserve.due_date
            }
    return render(request, 'tickets/ticket.html', data)


# Custom error
def handler404(request, exception, template_name='error/404.html'):
    return render(request, template_name)

def handler500(request, template_name='error/500.html'):
    return render(request, template_name)

def handler403(request, exception, template_name='error/403.html'):
    return render(request, template_name)

def handler400(request, exception, template_name='error/400.html'):
    return render(request, template_name)
