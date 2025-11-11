from django.contrib import admin
from django.urls import path, include

# Church App


urlpatterns = [
    path('admin/', admin.site.urls),
    path('form/', include('church_app.urls')), 
    path('api/', include('accounts.urls')),
    path('api/v1/mpesa/', include('payments.urls')),
]   
