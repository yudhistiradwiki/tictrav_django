from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings

from tictrav import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('tictrav.urls')), # TicTrav
    path('chatbot/',include('chatbot.urls')), # App chatbot
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


# Custom URL Error
handler404 = views.handler404
handler500 = views.handler500
handler403 = views.handler403