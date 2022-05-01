from django.contrib.auth import authenticate
from django.http import HttpResponse, JsonResponse
from app.models import User


def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")


def login(request):
    username = request.POST['username']
    password = request.POST['password']
    user = authenticate(username=username, password=password)
    print('user', user, username, password)
    return JsonResponse({'has_logged_in': bool(user)})
