from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from .models import *
from .forms import *

from django.contrib.auth import get_user_model
User = get_user_model()

def adminLogin(request):
    return HttpResponse("admin login")

def userLogin(request):
    return HttpResponse("user login")

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
    return render(request, "home.html", {})

def collection(request):
    if request.method == "POST":
        print(request.user.id)
        data = request.POST
        form = CollectionForm(data)
        if form.is_valid():
            print("success")
            collectionId = form.cleaned_data['collectionId']
            quantity = form.cleaned_data['quantity']
            initialPrice = form.cleaned_data['initialPrice']
            UserCollection.objects.create(
                uId = User.objects.get(id=request.user.id),
                collectionId = Collection.objects.get(collectionId = collectionId),
                quantity = quantity,
                initialPrice = initialPrice
            ).save()
            collections = Collection.objects.all()
            return render(request, "collection.html", {"form":form, "success": "collection added successfully", "collections": collections})
        else:
            print("failure")
            collections = Collection.objects.all()
            return render(request, 'collection.html', {"form":form, "collections": collections})
    else:
        print("hello")
        collections = Collection.objects.all()
        return render(request, 'collection.html', {"collections": collections})