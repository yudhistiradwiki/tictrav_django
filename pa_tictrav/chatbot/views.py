from django.shortcuts import render
from django.http import JsonResponse
from model_development import qas


from django.http import HttpResponse
import json

from django.views.decorators.csrf import csrf_exempt

from django.contrib import messages


from django.core.exceptions import PermissionDenied

# Model tourism
from tictrav import models

# Create your views here.

chatbot = None


@csrf_exempt
def getChatbotResponse(request):
	global chatbot

	if request.method=='POST':
		pertanyaan = request.POST['pertanyaan']

		tourism = models.TourismPlace.objects.all()
		
		if(not chatbot):
			try:
				chatbot = qas.chatbot(tourism)
			except:
				response = 'Chatbot sedang tidak dapat digunakan. Mohon maaf atas ketidaknyamanannya.'
		
		response = chatbot.getJawaban(pertanyaan)
				

		return JsonResponse({
			'jawaban': response
		})
	
	raise PermissionDenied
	
