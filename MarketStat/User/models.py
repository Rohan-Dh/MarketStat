from django.db import models
from django.conf import settings


class userProfile(models.Model):
    profileId = models.CharField(max_length=100, primary_key=True)
    userId = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    userName = models.CharField(max_length=100, null=False)
    profilePic = models.ImageField(upload_to='images/')
    address = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.userName
    
class Collection(models.Model):
    collectionId = models.AutoField(max_length=100, primary_key=True)
    cName = models.CharField(max_length=100, null=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.collectionId
    
class UserCollection(models.Model):
    ucId = models.AutoField(primary_key=True)
    uId = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='user_collections')
    collectionId = models.ForeignKey("Collection", on_delete=models.CASCADE)
    quantity = models.IntegerField()
    initialPrice = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.ucId

class Transaction(models.Model):
    transactionId = models.AutoField(primary_key=True)
    collectionId = models.ForeignKey('Collection', on_delete=models.DO_NOTHING)
    quantitySold = models.IntegerField()
    soldPrice = models.IntegerField()
    profit = models.IntegerField()
    soldTo = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.transactionId)

class Role(models.Model):
    rId = models.AutoField(primary_key=True)
    rName = models.CharField(max_length=100)
    
    def __str__(self):
        return self.rName

class Permission(models.Model):
    pId = models.AutoField(primary_key=True)
    pName = models.CharField(max_length=100)
    rolePermission = models.ManyToManyField("Role", related_name="role_permission")

    def __str__(self):
        return self.pName

class UserRole(models.Model):
    userRoleId = models.AutoField(primary_key=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    role = models.ForeignKey('Role', on_delete=models.CASCADE)

    class Meta:
        unique_together = ('user', 'role')