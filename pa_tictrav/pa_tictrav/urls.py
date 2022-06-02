from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings
<<<<<<< HEAD
=======

>>>>>>> 7c30f9f65313d318012d80f9ae4e0b265ee07026

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('tictrav.urls')), # TicTrav
    path('chatbot/',include('chatbot.urls')), # App chatbot
]
<<<<<<< HEAD
urlpatterns += static(settings.MEDIA_URL, 
document_root=settings.MEDIA_ROOT)
=======
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
>>>>>>> 7c30f9f65313d318012d80f9ae4e0b265ee07026
