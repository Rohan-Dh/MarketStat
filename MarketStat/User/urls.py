from django.urls import path, include
from .views import *

app_name = "user"

urlpatterns = [
    path("", userLogin, name="userLogin"),
    path('home/', home, name="home"),
    path("accounts/", include("django.contrib.auth.urls")),
    path('login/', adminLogin, name="adminLogin"),
    path('signup/', authView, name="authView"),
    path('collection/', collection, name="collection"),
]