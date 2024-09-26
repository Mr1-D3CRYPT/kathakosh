from django.shortcuts import render
import pprint
import google.generativeai as palm
palm.configure(api_key='AIzaSyAT1VQThfonpDb9Rexw__6aipCcrgcrxv0')


# Create your views here.
def index(request):
    model = palm.GenerativeModel('gemini-pro')

    prompt = "Create one story for kids of 5 years age on the genre adventure. Each time create an unique story"
    response = model.generate_content(prompt)

    response.text 
    
    return render(request, 'index.html')