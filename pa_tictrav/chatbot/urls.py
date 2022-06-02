from django.urls import path
from chatbot import views


app_name = 'chatbot'


urlpatterns=[
	# Pass
	path('ask-question/', views.getChatbotResponse, name='getAnswerChatbot')

]