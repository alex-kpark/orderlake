from django.shortcuts import render
from django.http import HttpResponse, JsonResponse

# Create your views here.

def testing(request):
    print(request)
    return HttpResponse('success')