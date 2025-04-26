from django.urls import path
from . import views

urlpatterns = [
    path('createUser/', views.createUser, name="createUser"),
]