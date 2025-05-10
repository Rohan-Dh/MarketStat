from django.urls import path, include
from .views import *

app_name = "user"

urlpatterns = [
    # path("", userLogin, name="userLogin"),
    path('home/', home, name="home"),
    path("", CustomLoginView.as_view(), name='login'),
    path("accounts/", include("django.contrib.auth.urls")),
    path('logout/', logout, name="logout"),
    path('signup', authView, name="authView"),
    path('collection/', collection, name="collection"),
    path('collection/delete/<int:userCollectionId>/', deleteCollection, name='deleteCollection'),
    path('collection/update/<int:userCollectionId>/', updateCollection, name='updateCollection'),
    path('collection/sell/<int:userCollectionId>/', sellCollection, name='sellCollection'),
    path('notification/', notification, name="notification"),
    path('profile/<int:userId>/', profileView, name="profile"),
    path('profile/change-profile/', changeProfile, name='changeProfile'),
    path('verifyEmail/', verifyEmail, name='verifyEmail'),
    path('sale-analysis/', saleAnalysis, name='saleAnalysis'),
    path('display-graph/', displayGraph, name='displayGraph'),
]