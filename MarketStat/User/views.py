from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from django.http import HttpResponse
from django.contrib import auth
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
    userCollections = UserCollection.objects.filter(userId = request.user.id)
    serializer = CollectionUserCollectionSerializer(userCollections, many=True).data
    collections = Collection.objects.all()

    if request.method == "POST":
        form = CollectionForm(request.POST)
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
            return redirect('user:collection')
        return render(
                request, 
                'collection.html',
                {
                    "form":form, 
                    "collections": collections, 
                    "userCollections": serializer,
                    })
    return render(
            request, 
            'collection.html', 
            {
                "collections": collections, 
                "userCollections": serializer,
                })
    
    
@login_required
def logout(request):
    auth.logout(request)
    return redirect('/')

@login_required
def updateCollection(request, userCollectionId):
    userCollections = UserCollection.objects.filter(userId = request.user.id)
    serializer = CollectionUserCollectionSerializer(userCollections, many=True).data
    collections = Collection.objects.all()
    if request.method == "POST":
        form = updateForm(request.POST)
        if not form.is_valid():
            return render(request, "collection.html", {
                "form": form,
                "collections": collections,
                "userCollections": serializer
            })
        
        collectionObject = get_object_or_404(UserCollection, userCollectionId=userCollectionId)
        collectionObject.quantity = form.cleaned_data['changedQuantity']
        collectionObject.initialPrice = form.cleaned_data['changedPrice']
        collectionObject.save()
        return redirect('user:collection')
    return redirect('user:collection')

@login_required
def deleteCollection(request, userCollectionId):
    try:
        userCollectionObject = UserCollection.objects.filter(userCollectionId = userCollectionId)
    except UserCollection.DoesNotExist:
        error = "collection doesn't exists"
        return redirect("user:collection")
    userCollectionObject.delete()
    return redirect("user:collection")

@login_required
def sellCollection(request, userCollectionId):
    if request.method != "POST":
        return redirect('user:collection')

    form = SellForm(request.POST)
    user_collection = get_object_or_404(UserCollection, userCollectionId=userCollectionId)
    collections = Collection.objects.all()
    user_collections = UserCollection.objects.filter(userId=request.user.id)
    user_collection_data = CollectionUserCollectionSerializer(user_collection).data
    all_collections_data = CollectionUserCollectionSerializer(user_collections, many=True).data

    if not form.is_valid():
        return render(request, 'collection.html', {
            "form": form,
            "collections": collections,
            "userCollections": all_collections_data,
        })

    sold_to = form.cleaned_data['soldTo']
    sold_quantity = form.cleaned_data['soldQuantity']
    sold_price = form.cleaned_data['soldPrice']

    if sold_quantity > user_collection_data["quantity"]:
        return render(request, 'collection.html', {
            "error": ["You don't have that much quantity"],
            "context": {"showPopUp": True},
            "collections": collections,
            "userCollections": all_collections_data,
        })

    profit_or_loss = sold_price - user_collection_data["initialPrice"]
    Transaction.objects.create(
        quantitySold=sold_quantity,
        user_collection=user_collection,
        soldPrice=sold_price,
        soldTo=sold_to,
        profit=profit_or_loss if profit_or_loss > 0 else 0,
        loss=-profit_or_loss if profit_or_loss < 0 else 0
    )

    user_collection.quantity -= sold_quantity
    user_collection.save()

    return redirect('user:collection')

@login_required
def notification(request):
    userCollections = list(UserCollection.objects.filter(userId = request.user.id).values())
    userCollections = [collection["userCollectionId"] for collection in userCollections]
    transactions = Transaction.objects.filter(user_collection__in = userCollections).values()
    return render(request, 'notification.html', {'transactions': transactions})