from django.urls import path
from . import views

# Church App Urls
urlpatterns = [
    path('prayer/', views.prayer_form_view, name='prayer_form'),
]