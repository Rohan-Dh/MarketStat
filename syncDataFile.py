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
        if Role.objects.filter(roleName = role).exists():
            print(f"{role} already exists")
            continue
        else:
            roleObject = Role.objects.create(roleName = role)
            print(f"Role {role} created successfully")

def createPermission():
    permissions = [
        "create-user",
        "delete-user",
    ]
    for permission in permissions:
        if Permission.objects.filter(permissionName = permission).exists():
            print(f"{permission} already exists")
            continue
        else:
            permissionObject = Permission.objects.create(permissionName = permission)
            print(f"Permission {permission} created successfully")

def assignPermission():
    adminRole = Role.objects.get(roleName = "admin")
    userRole = Role.objects.get(roleName = "user")

    create_user = Permission.objects.get(permissionName = "create-user")
    delete_user = Permission.objects.get(permissionName = "delete-user")
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
    "Kurtis and tunics",
    "Sarees",
    "Salwar suits",
    "Leggings and jeggings",
    "Skirts",
    "Jeans and pants",
    "Shrugs and jackets",
    "Dupattas and stoles",
    ]

    existingCollections = list(Collection.objects.all().values())
    existingCollectionName = set([existingCollection["collectionName"] for existingCollection in existingCollections])

    collectionObject = set([collection for collection in collections])
    collectionObjects = collectionObject - existingCollectionName

    print(collectionObjects)
    if len(list(collectionObjects)) == 0:
        print("No new element to add")
        return
    else:
        for collectionObject in list(collectionObjects):
            collection = Collection()
            collection.collectionName = collectionObject
            collection.save()
        print("Collection added successfully")

addUsers()
createPermission()
createRole()
assignPermission()
feedCollection()