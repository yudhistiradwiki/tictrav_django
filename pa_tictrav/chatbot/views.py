from django.shortcuts import render
from django.http import JsonResponse
from model_development import qas


from django.http import HttpResponse
import json

from django.views.decorators.csrf import csrf_exempt

from django.http import Http404


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

		print(pertanyaan)
		
		if(not chatbot):
			try:
				tourism = models.TourismPlace.objects.all()
			except:
				raise Http404()
			else:
				chatbot = qas.chatbot(tourism)

		return JsonResponse({
			'jawaban': chatbot.getJawaban(pertanyaan)
		})
	
	raise PermissionDenied
	
