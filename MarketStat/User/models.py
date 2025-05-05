from django.db import models
from django.conf import settings


class UserProfile(models.Model):
    profileId = models.AutoField(primary_key=True)
    userId = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    userName = models.CharField(max_length=100, null=False, default="Unknown")
    profilePic = models.ImageField(upload_to='images/', default=None, null=True)
    address = models.CharField(max_length=100, null=True, default=None)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.userName
    
class Collection(models.Model):
    collectionId = models.AutoField(primary_key=True)
    collectionName = models.CharField(max_length=100, null=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.collectionId
    
class UserCollection(models.Model):
    userCollectionId = models.AutoField(primary_key=True)
    userId = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='user_collections')
    collectionId = models.ForeignKey("Collection", on_delete=models.CASCADE)
    quantity = models.IntegerField()
    initialPrice = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.userCollectionId)

class Transaction(models.Model):
    transactionId = models.AutoField(primary_key=True)
    user_collection = models.ForeignKey(
        'UserCollection', 
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )
    quantitySold = models.IntegerField()
    soldPrice = models.IntegerField()
    profit = models.IntegerField(default=None, null=True)
    loss = models.IntegerField(default=None, null=True)
    soldTo = models.CharField(max_length=100, default=None, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return str(self.transactionId)

class Role(models.Model):
    roleId = models.AutoField(primary_key=True)
    roleName = models.CharField(max_length=100)
    
    def __str__(self):
        return self.roleName

class Permission(models.Model):
    permissionId = models.AutoField(primary_key=True)
    permissionName = models.CharField(max_length=100)
    rolePermission = models.ManyToManyField("Role", related_name="role_permission")

    def __str__(self):
        return self.permissionName

class UserRole(models.Model):
    userRoleId = models.AutoField(primary_key=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    role = models.ForeignKey('Role', on_delete=models.CASCADE)

    class Meta:
        unique_together = ('user', 'role')