from django.shortcuts import render
from django.http import JsonResponse

def index(request):
    print(request.user.socialaccount_set.all()[0].extra_data)
    output = {
        'status': 'Success',
        'message': 'App running flawlessly',
        'data': None
    }
    return JsonResponse(output, status=200)
