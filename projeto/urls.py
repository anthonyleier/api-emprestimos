from django.contrib import admin
from django.urls import path, include


urlpatterns = [
    path('api/', include('onedata.urls')),
    path('admin/', admin.site.urls),
]
