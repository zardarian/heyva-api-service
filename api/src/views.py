from django.shortcuts import render
from django.http import JsonResponse

def index(request):
    output = {
        'status': 'Success',
        'message': 'App running flawlessly',
        'data': None
    }
    return JsonResponse(output, status=200)
