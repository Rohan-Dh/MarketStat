from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from django.contrib.auth.views import LoginView
from django.db.models import Sum
from django.utils import timezone
from datetime import timedelta
from django.http import HttpResponse, JsonResponse
from django.contrib import auth
from datetime import datetime
from .serializers import *
from .models import *
from .forms import *

from django.contrib.auth import get_user_model
User = get_user_model()

class CustomLoginView(LoginView):
    redirect_authenticated_user = True
    template_name = 'registration/login.html'
    def form_valid(self, form):
        remember_me = self.request.POST.get('remember_me', False)
        if not remember_me:
            self.request.session.set_expiry(0)
            self.request.session.modified = True
        else:
            print("success")
            self.request.session.set_expiry(30*24*60*60)
            self.request.session.modified = True
        return super().form_valid(form)

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
    CollectionsIds = [collection['collectionId_id'] for collection in list(userCollections.values())]
    success = False
    error = False

    if request.method == "POST":
        if int(request.POST.get('collectionId')) in CollectionsIds:
            request.session['error'] = f"{Collection.objects.get(collectionId = request.POST.get('collectionId')).collectionName} already exists. Try updating it."
            return redirect('user:collection')
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
            request.session['success'] = f"Collection {Collection.objects.get(collectionId=collectionId).collectionName} added successfully"
            return redirect('user:collection')
        # return JsonResponse(form.errors, safe=False)
        request.session['form'] = form.errors
        return redirect('user:collection')
    form = CollectionForm()
    if "form" in request.session:
        form = request.session.pop('form')
    if 'success' in request.session:
        success = request.session.pop('success')
    if 'error' in request.session:
        error = request.session.pop('error')
    return render(
            request, 
            'collection.html', 
            {
                "error": error,
                "form": form,
                "collections": collections, 
                "userCollections": serializer,
                "success": success
                })
    
    
@login_required
def logout(request):
    auth.logout(request)
    return redirect('/')

@login_required
def updateCollection(request, userCollectionId):
    userCollections = UserCollection.objects.filter(userId=request.user.id)
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
        oldCollectionName = collectionObject.collectionId.collectionName
        newCollection = Collection.objects.get(collectionId=request.POST["collectionId"])
        newCollectionName = newCollection.collectionName

        quantitySame = collectionObject.quantity == form.cleaned_data['changedQuantity']
        priceSame = collectionObject.initialPrice == form.cleaned_data['changedPrice']
        print(collectionObject.collectionId == newCollection)
        collectionSame = collectionObject.collectionId == newCollection

        # All 3 changed
        if not collectionSame and not quantitySame and not priceSame:
            request.session['success'] = (
                f"{oldCollectionName} changed to {newCollectionName}\n"
                f"with Quantity changed from {collectionObject.quantity} to {form.cleaned_data['changedQuantity']} and\n"
                f"Cost Price changed from {collectionObject.initialPrice} to {form.cleaned_data['changedPrice']}"
            )

        # Collection and Quantity changed
        elif not collectionSame and not quantitySame and priceSame:
            request.session['success'] = (
                f"{oldCollectionName} changed to {newCollectionName}\n"
                f"with Quantity changed from {collectionObject.quantity} to {form.cleaned_data['changedQuantity']}"
            )

        # Collection and Price changed
        elif not collectionSame and quantitySame and not priceSame:
            request.session['success'] = (
                f"{oldCollectionName} changed to {newCollectionName}\n"
                f"with Cost Price changed from {collectionObject.initialPrice} to {form.cleaned_data['changedPrice']}"
            )

        # Quantity and Price changed (same collection)
        elif collectionSame and not quantitySame and not priceSame:
            request.session['success'] = (
                f"Quantity changed from {collectionObject.quantity} to {form.cleaned_data['changedQuantity']}\n"
                f"Cost Price changed from {collectionObject.initialPrice} to {form.cleaned_data['changedPrice']}"
            )

        # Only Collection changed
        elif not collectionSame and quantitySame and priceSame:
            request.session['success'] = f"{oldCollectionName} changed to {newCollectionName}"

        # Only Quantity changed
        elif collectionSame and not quantitySame and priceSame:
            request.session['success'] = f"Quantity changed from {collectionObject.quantity} to {form.cleaned_data['changedQuantity']}"

        # Only Price changed
        elif collectionSame and quantitySame and not priceSame:
            request.session['success'] = f"Cost Price changed from {collectionObject.initialPrice} to {form.cleaned_data['changedPrice']}"

        # No changes
        else:
            request.session['success'] = "No changes were made."

        collectionObject.quantity = form.cleaned_data['changedQuantity']
        collectionObject.initialPrice = form.cleaned_data['changedPrice']
        collectionObject.collectionId = newCollection
        collectionObject.save()
        return redirect('user:collection')

    return redirect('user:collection')


@login_required
def deleteCollection(request, userCollectionId):
    userCollectionObject = UserCollection.objects.get(userCollectionId = userCollectionId)
    userCollectionObject.delete()
    request.session['success'] = f"{userCollectionObject.collectionId.collectionName} deleted successfully"
    return redirect("user:collection")

@login_required
def sellCollection(request, userCollectionId):
    collections = Collection.objects.all()
    user_collection = get_object_or_404(UserCollection, userCollectionId=userCollectionId)
    user_collection_data = CollectionUserCollectionSerializer(user_collection).data
    user_collections = UserCollection.objects.filter(userId=request.user.id)
    all_collections_data = CollectionUserCollectionSerializer(user_collections, many=True).data

    if request.method == "POST":
        form = SellForm(request.POST)
        if not form.is_valid():
            request.session['form'] = form.errors
            request.session['check'] = True
            return redirect('user:sellCollection', userCollectionId)

        sold_to = form.cleaned_data['soldTo']
        sold_quantity = form.cleaned_data['soldQuantity']
        sold_price = form.cleaned_data['soldPrice']

        if sold_quantity > user_collection_data["quantity"]:
            request.session['greaterSellingQuantityError'] = "You don't have that much quantity"
            request.session['check'] = True
            return redirect('user:sellCollection', userCollectionId)

        profit_or_loss = sold_price - user_collection_data["initialPrice"]
        Transaction.objects.create(
            quantitySold=sold_quantity,
            user_collection=user_collection,
            soldPrice=sold_price,
            soldTo=sold_to,
            profit=sold_quantity * profit_or_loss if profit_or_loss > 0 else 0,
            loss= sold_quantity * -profit_or_loss if profit_or_loss < 0 else 0
        )

        user_collection.quantity -= sold_quantity
        user_collection.save()
        # return JsonResponse(user_collection_data, safe=False)
        request.session['success'] = f"Sold {sold_quantity} {Collection.objects.get(collectionId = user_collection_data["collection"]["collectionId"]).collectionName} for amount {sold_price}"
        return redirect('user:sellCollection', userCollectionId)
    
    greaterSellingQuantityError = None
    check = False
    form = None
    success = False
    if 'greaterSellingQuantityError' in request.session:
        greaterSellingQuantityError = request.session.pop('greaterSellingQuantityError')
    if 'check' in request.session:
        check = request.session.pop('check')
    if 'form' in request.session:
        form = request.session.pop('form')
    if 'success' in request.session:
        success = request.session.pop('success')
    return render(request, 'collection.html', {
        'form': form,
        'check': check,
        'greaterSellingQuantityError': greaterSellingQuantityError,
        'collections': collections,
        'userCollections': all_collections_data,
        'success': success
    })

@login_required
def notification(request):
    userCollections = list(UserCollection.objects.filter(userId = request.user.id).values())
    userCollections = [collection["userCollectionId"] for collection in userCollections]
    transactions = Transaction.objects.filter(user_collection__in = userCollections)
    serializer = TransactionSerializer(transactions, many=True)
    # return JsonResponse(serializer.data, safe=False)
    return render(request, 'notification.html', {'transactions': serializer.data})

@login_required
def profileView(request, userId=None):
    error = False
    if 'error' in request.session:
        error = request.session.pop('error')

    profile = UserProfile.objects.get(userId=request.user.id)
    profile_data = UserProfileSerializer(profile).data

    if request.method == "POST":
        form = UserProfileForm(request.POST, request=request)
        if form.is_valid():
            firstName = form.cleaned_data["firstName"]
            lastName = form.cleaned_data["lastName"]
            address = form.cleaned_data["address"]
            email = form.cleaned_data["email"]

            profileObj = get_object_or_404(UserProfile, userId=userId)
            userObj = get_object_or_404(User, id=userId)
            userObj.first_name = firstName
            userObj.last_name = lastName
            profileObj.address = address
            profileObj.userName = firstName + " " + lastName if lastName else ""
            userObj.save()
            profileObj.save()

            if profileObj.email_verified and userObj.email == email:
                request.session['show_code_form'] = False
            else:
                request.session['show_code_form'] = True

            request.session['submitted_email'] = email
            return redirect('user:profile', userId=userId)
        return redirect('user:profile', userId=userId)
    
    form = UserProfileForm()
    show_code_form = request.session.pop('show_code_form', False)
    email = request.session.pop('submitted_email', profile.userId.email)

    return render(request, 'profile.html', {
        'form': form,
        'userProfile': profile_data,
        'show_code_form': show_code_form,
        'email': email,
        'error': error,
    })



@login_required
def changeProfile(request):
    return HttpResponse("Change Profile")

@login_required
def verifyEmail(request):
    if request.method == "POST":
        data = request.POST
        inputCode = data['firstNumber'] + data['secondNumber'] + data['thirdNumber'] +data['forthNumber']
        actualCode = data["actualCode"]
        if inputCode == actualCode:
            userObj = get_object_or_404(User, id = request.user.id)
            profileObj = get_object_or_404(UserProfile, userId = request.user.id)
            userObj.email = data['email']
            request.session['submitted_email'] = data['email']
            profileObj.email_verified = True
            userObj.save()
            profileObj.save()
            request.session['success'] = "Email has been changed."
            return redirect('user:profile', userId = request.user.id)
        else:
            request.session['submitted_email'] = data['email']
            request.session['show_code_form'] = True
            request.session['error'] = "Email is not verified. Code doesn't match"
            return redirect('user:profile', userId = request.user.id)


        
@login_required
def saleAnalysis(request):
    if request.method == "POST":
        time_interval = request.POST.get('time_interval')
        start_date = request.POST.get('start_date')
        end_date = request.POST.get('end_date')

        if time_interval:
            today = timezone.now().date()
            
            if time_interval == 'today':
                start_date = today
                end_date = today
            elif time_interval == 'week':
                start_date = today - timedelta(days=today.weekday())
                end_date = start_date + timedelta(days=6)
            elif time_interval == 'month':
                start_date = today.replace(day=1)
                end_date = (start_date + timedelta(days=31)).replace(day=1) - timedelta(days=1)
            
            request.session['start_date'] = str(start_date)
            request.session['end_date'] = str(end_date)
        
        elif start_date and end_date:
            request.session['start_date'] = str(start_date)
            request.session['end_date'] = str(end_date)

        return redirect("user:saleAnalysis")
    
    start_date = timezone.now().date()
    end_date = timezone.now().date()

    if 'start_date' in request.session and 'end_date' in request.session:
        start_date = datetime.strptime(request.session.pop('start_date'), "%Y-%m-%d").date()
        end_date = datetime.strptime(request.session.pop('end_date'), "%Y-%m-%d").date()
    
    collection_data = Transaction.objects.filter(
            created_at__date__range=[start_date, end_date]
        )

    userCollectionIds = UserCollection.objects.filter(userId=request.user).values_list('pk', flat=True)
    collection_data = (collection_data.filter(user_collection__in = userCollectionIds)
                    .values(
                        'user_collection_id',
                        'user_collection__collectionId',
                        'user_collection__collectionId__collectionName'
                        )
                    .annotate(
                        quantitySold = Sum('quantitySold'),
                        soldPrice = Sum('soldPrice'),
                        totalProfit = Sum('profit'),
                        totalLoss = Sum('loss')
                        ))
    collection_data = [
        {
            'userCollectionId': entry['user_collection_id'],
            'collectionId': entry['user_collection__collectionId'],
            'collectionName': entry['user_collection__collectionId__collectionName'],
            'quantitySold': entry['quantitySold'],
            'soldPrice': entry['soldPrice'],
            'totalProfit': entry['totalProfit'],
            'totalLoss': entry['totalLoss'],
        }
        for entry in collection_data
    ]
    collection_data = sorted(collection_data, key=lambda x: x['quantitySold'], reverse=True)
    # return JsonResponse(collection_data, safe=False)


    # Calculate percentages
    soldPrice = sum(item['soldPrice'] for item in collection_data) or 1
    for item in collection_data:
        item['percentage'] = round((item['soldPrice'] / soldPrice) * 100, 2)
    
    context = {
        'collection_data': collection_data,
    }
    return render(request, 'saleAnalysis.html', context)


@login_required
def displayGraph(request):
    return HttpResponse("hello")