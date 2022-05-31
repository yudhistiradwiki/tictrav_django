from django.shortcuts import render
from django.http.response import HttpResponse
from io import BytesIO
from django.views import View
from django.template.loader import get_template
from xhtml2pdf import pisa
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.conf import settings

# Create your views here.

#Login
def login(request):
    username = ["yudhistiradwiki", "steven", "rijal", "nicky", "diky"]
    password = "pass"

    konteks = {
        'user': username,
        'pass': password,
    }
    return render(request, 'login.html', konteks)

#Register
def register(request):
     return render(request, 'register.html')

#Home
@login_required(login_url=settings.LOGIN_URL)
def index(request):
     return render(request, 'index.html')

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

def desc(request):
     return render(request, 'desc.html')

def coba(request):
     return render(request, 'coba.html')