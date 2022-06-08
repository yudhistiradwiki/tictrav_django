from ctypes.wintypes import INT
from django.shortcuts import render, redirect
from django.http.response import HttpResponse
from io import BytesIO
from django.views import View
from django.template.loader import get_template
from xhtml2pdf import pisa
from django.contrib import messages
# from django.contrib.auth.decorators import login_required
from django.conf import settings


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
# @login_required(login_url=settings.LOGIN_URL)
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
        if model_predict == None:
            model_predict = md.Model('ModelUserAgeTourismConcate(Dipake)',data)
        
        recommend = model_predict.predict(request.user.id,request.user.age)
        recommend = models.TourismPlace.objects.filter(pk__in=recommend)

    # tourism = models.TourismPlace.objects.values('city').annotate(jum_city=Count('city')).order_by()
    return render(request, 'home.html',{'tourism': tourism,'recommend':recommend})

def desc(request, placeid):
    global model_statictis_item
    tourism = models.TourismPlace.objects.get(place_id=placeid)

    reservation = models.Reservation.objects.all()
    data = {
        'user':[i.user for i in reservation],
        'place':[i.place for i in reservation],
        'place_ratings':[i.place_ratings for i in reservation]
    }

    # Inisialisasi model hanya sekali
    if model_statictis_item == None:
        # 0 user 1 item
        model_statictis_item = md.colaborative_calculation_statistik(data,"place",1)

    # Penghapusan karakter place_ hasil get_dummies
    recommend = [re.sub('place_','',i) for i in model_statictis_item.itemRecommendedByItem(tourism.place_id, 5)]
    recommend = models.TourismPlace.objects.filter(pk__in=recommend)

    return render(request, "desc.html", {'data':tourism, 'recommend':recommend})


def editProfile(request):
    if request.method=='POST' and request.user.is_authenticated:
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


"""
    Pemesanan reservasi
"""
# Reservasi
def reservasi(request,placeid):
    tourism = models.TourismPlace.objects.get(place_id=placeid)
    user = models.AccountCustom.objects.get (id = request.user.id)
    if request.method == 'POST' and request.user.is_authenticated:
        _, fullname, email, phone, location, due_date = request.POST.values()
        
        # Update akun bila ada perubahan
        account = models.AccountCustom.objects.get(id=request.user.id)
        account.full_name = fullname
        account.location = location
        account.email = email
        account.phone_number = phone
        account.save()
        reservasi_user = models.Reservation.objects.create(user = user , place = tourism, due_date = request.POST['due_date']) 
        reservasi_user.save()
        return redirect(f'/desc/{placeid}')
    try:
        reservasi_form =  forms.ReservationForm(instance=request.user)
    except:
        return redirect('/login')

    return render(request, "pemesanan.html",{'reservation':reservasi_form,'tourism':tourism})


#Ticket
def render_pdf(template_src, context_dict={}):
    template = get_template(template_src)
    html = template.render(context_dict)
    result = BytesIO()
    pdf = pisa.pisaDocument(BytesIO(html.encode("ISO-8859-1")), result)
    if not pdf.err:
        return HttpResponse(result.getvalue(), content_type='application/pdf')
    return None

data = {
    "nama" : "Dwiki",
    "wisata" : "Monumen Nasional"
}

class ViewPDF(View):
    def get(self, request, *args, **kwargs):
        pdf = render_pdf('ticket.html', data)
        return HttpResponse(pdf, content_type='application/pdf')


def ticket(request):
     return render(request, 'ticket.html')

