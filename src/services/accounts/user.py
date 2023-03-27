from django.http import JsonResponse
from django.shortcuts import render


def index(request):
    return JsonResponse({'test': 'hello2'})
