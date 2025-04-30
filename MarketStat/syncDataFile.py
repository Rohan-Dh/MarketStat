import os
import django
from django.contrib.auth.hashers import make_password

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'MarketStat.settings')
django.setup()

from User.models import *
from django.contrib.auth import get_user_model
User = get_user_model()

def addUsers():
    data ={
        "username": "USER2",
        "password": "12345678",
    }
    if User.objects.filter(username = data['username']).exists():
        print(f"user with username {data['username']} already exists")
    else:
        User.objects.create_user(
            username = data['username'],
            password = make_password(data['password'])
        )

def createRole():
    roles = ["user", "admin"]
    for role in roles:
        if Role.objects.filter(rName = role).exists():
            print(f"{role} already exists")
            continue
        else:
            roleObject = Role.objects.create(rName = role)
            print(f"Role {role} created successfully")

def createPermission():
    permissions = [
        "create-user",
        "delete-user",
    ]
    for permission in permissions:
        if Permission.objects.filter(pName = permission).exists():
            print(f"{permission} already exists")
            continue
        else:
            permissionObject = Permission.objects.create(pName = permission)
            print(f"Permission {permission} created successfully")

def assignPermission():
    adminRole = Role.objects.get(rName = "admin")
    userRole = Role.objects.get(rName = "user")

    create_user = Permission.objects.get(pName = "create-user")
    delete_user = Permission.objects.get(pName = "delete-user")
    try:
        adminRole.role_permission.add(*[create_user, delete_user])
    except Exception as e:
        print(e)

def feedCollection():
    collections = [
    "T-shirts",
    "Shirts (formal/casual)",
    "Trousers",
    "Jeans",
    "Shorts",
    "Track pants",
    "Jackets",
    "Suits and blazers",
    "Kurta pyjama sets",
    "Sherwanis",
    "Hoodies and sweatshirts",
    "Baby rompers",
    "T-shirts and tops",
    "Jeans and shorts",
    "Frocks",
    "Skirts",
    "Jackets",
    "Ethnic wear for kids",
    "Tops and blouses",
    "T-shirts",
    "Dresses (casual, party, gowns)",
    "Kurtis and tunics",
    "Sarees",
    "Salwar suits",
    "Leggings and jeggings",
    "Skirts",
    "Jeans and pants",
    "Shrugs and jackets",
    "Dupattas and stoles",]
    
    collectionObject = [Collection(cName = collection) for collection in collections]
    Collection.objects.bulk_create(collectionObject)

addUsers()
createPermission()
createRole()
assignPermission()
feedCollection()