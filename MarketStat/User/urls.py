from django.urls import path, include
from .views import *

app_name = "user"

urlpatterns = [
    # path("", userLogin, name="userLogin"),
    path('home/', home, name="home"),
    path("accounts/", include("django.contrib.auth.urls")),
    path('login/', adminLogin, name="adminLogin"),
    path('logout/', logout, name="logout"),
    path('', authView, name="authView"),
    path('collection/', collection, name="collection"),
    path('collection/delete/<int:Collection_id>/', deleteCollection, name='deleteCollection'),
    path('collection/update/<int:Collection_id>/', updateCollection, name='updateCollection'),
    path('collection/sell/<int:Collection_id>/', sellCollection, name='sellCollection'),
]