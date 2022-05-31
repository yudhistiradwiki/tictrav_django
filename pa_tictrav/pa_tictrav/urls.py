from django.contrib import admin
from django.urls import path, include


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('tictrav.urls')), # TicTrav
    # path('',include('chatbot.urls')), # App chatbot
]
