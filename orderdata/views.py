from django.shortcuts import render
from django.http import HttpResponse, JsonResponse

# Create your views here.

def testing(request):
    return render(request, 'showing/post_list.html', {})

def testing_test(request):
    return render(request, 'showing/post_list2.html', {})