from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.contrib import auth
from rest_framework.response import Response
from .serializers import *
from .models import *
from .forms import *

from django.contrib.auth import get_user_model
User = get_user_model()

def adminLogin(request):
    return HttpResponse("admin login")


def authView(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST or None)
        if form.is_valid():
            form.save()
            return redirect("user:login")
    else:
        form = UserCreationForm()
    return render(request, 'registration/signup.html', {"form": form})

@login_required
def home(request):
    userId = request.user.id
    if not UserProfile.objects.filter(userId = userId).exists():
        UserProfile.objects.create(
            userId = User.objects.get(id = userId)
        ).save()
    userDetails = UserProfile.objects.get(userId = userId)
    try:
        collections = UserCollection.objects.filter(uId = userId)
    except Exception as e:
        return render(request, "home.html", {"error": e, "userDetails": userDetails})
    return render(request, "home.html", {"collections": collections, "userDetails": userDetails})

@login_required
def collection(request):
    try:
        userCollections = UserCollection.objects.filter(userId = request.user.id)
    except UserCollection.DoesNotExist:
        return render(request, "collection.html")
    if request.method == "POST":
        data = request.POST
        form = CollectionForm(data)
        if form.is_valid():
            collectionId = form.cleaned_data['collectionId']
            quantity = form.cleaned_data['quantity']
            initialPrice = form.cleaned_data['initialPrice']
            UserCollection.objects.create(
                userId = User.objects.get(id=request.user.id),
                collectionId = Collection.objects.get(collectionId = collectionId),
                quantity = quantity,
                initialPrice = initialPrice
            ).save()
            collections = Collection.objects.all()
            return redirect('user:collection')
        else:
            collections = Collection.objects.all()
            userCollections = UserCollection.objects.filter(userId = request.user.id)
            serializer = CollectionUserCollectionSerializer(userCollections, many=True)
            return Response(serializer.data)
            return render(
                request, 
                'collection.html', 
                {
                    "form":form, 
                    "collections": collections, 
                    "userCollections": userCollections,
                    })
    else:
        collections = Collection.objects.all()
        return render(
            request, 
            'collection.html', 
            {
                "collections": collections, 
                "userCollections": userCollections,
                })
    
    
@login_required
def logout(request):
    auth.logout(request)
    return redirect('/')

@login_required
def updateCollection(request, Collection_id):
    return HttpResponse("update")

@login_required
def deleteCollection(request, Collection_id):
    return HttpResponse("delete")

@login_required
def sellCollection(request, Collection_id):
    return HttpResponse("sell")