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
from tictrav import models
from django.db.models import Count

from model_development import model as md


# Create your views here.
model_statictis = None
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
        
# def login(request):
#     username = ["yudhistiradwiki", "steven", "rijal", "nicky", "diky"]
#     password = "pass"

#     konteks = {
#         'user': username,
#         'pass': password,
#     }
#     return render(request, 'login.html', konteks)

# Register
def register(request):
     if request.method=='POST':
        _, fullname, age, email, password = request.POST.values()

        try:
            user = models.AccountCustom.objects.create_user(email,password,fullname,age)
        except:
            return redirect("/login",{'message':'User telah terdaftar'})
        else:
            user.save()

     return redirect("/login")



# Logout
def logout(request):
    logout(request)
    return redirect("/")


#Home
# @login_required(login_url=settings.LOGIN_URL)
# def home(request):
#      return render(request, 'home.html')
def index(request):
    recommend = None
    tourism = models.TourismPlace.objects.all()
    data = {
        'place_id':[i.place_id for i in tourism],
        'place_name':[i.place_name for i in tourism],
        'category':[i.category for i in tourism],
    }
    if request.user.is_authenticated:
        print(request.user.id," ",request.user.age)
        recommend = md.Model('ModelUserAgeTourismConcate(Dipake)',data).predict(request.user.id,request.user.age)
        recommend = models.TourismPlace.objects.filter(pk__in=recommend)

    # tourism = models.TourismPlace.objects.values('city').annotate(jum_city=Count('city')).order_by()
    return render(request, 'home.html',{'tourism': tourism,'recommend':recommend})




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

def desc(request, placeid):
    global model_statictis
    tourism = models.TourismPlace.objects.get(place_id=placeid)

    reservation = models.Reservation.objects.all()
    data = {
        'user':[i.user for i in reservation],
        'place':[i.place for i in reservation],
        'place_ratings':[i.place_ratings for i in reservation]
    }

    # Inisialisasi model hanya sekali
    if not model_statictis:
        model_statictis = md.colaborative_calculation_statistik(data,"place")
    
    recommend = model_statictis.itemRecommendedByItem(tourism.place_name, 5)

    return render(request, "desc.html", {'data':tourism, 'recommend':recommend})

def coba(request):
     return render(request, 'coba.html')

def rekomendasi(request):
    data = models.TourismPlace.objects.all()
    return render(request, "desc.html", {'data':data})
