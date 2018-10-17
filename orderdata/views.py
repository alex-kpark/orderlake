from django.shortcuts import render
from django.http import HttpResponse, JsonResponse

from orderdata.SsobingDownloader import * #django에서 import 할 때는 App이름.함수 형태로 import

# Runserver 하면 Views.py는 자동으로 수행되기 시작

# Login은 일단 하고 시작
def login_to_ssobing(request):
    return('connected')
    id = 'pineappleshop'
    pw = 'joejoe11!!'
    ssobing_login(id, pw)

def batch_downloader():
    pass

def testing():
    pass
    