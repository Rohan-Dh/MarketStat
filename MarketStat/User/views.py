from django.shortcuts import render
from django.http import HttpResponse, JsonResponse

def createUser(request):
    if checkPermission(request):
        return HttpResponse("valid user")
    return HttpResponse("invalid user")