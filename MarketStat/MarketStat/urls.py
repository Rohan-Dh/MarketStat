from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('admin/', admin.site.urls),
    path('admin-login/', include('User.urls')),
    path('', include('User.urls')),
] + static(settings.STATIC_URL)