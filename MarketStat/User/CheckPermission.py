from .models import *
from django.contrib.auth import get_user_model
User = get_user_model()

createCollection = "create-collection",
updateCollection = "update-collection",
deleteCollection = "delete-collection",
viewCollection = "view-collection",

# def checkPermission(request, permission):
#     userId = request.user.id
#     try:
#         user = User.objects.get(id = userId)
        
