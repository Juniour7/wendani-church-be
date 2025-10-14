from django.urls import path
from . import views
from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [
    path('token/', views.login_view, name='login'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('logout/', views.logout_view, name='logout'),

    # User management
    path('me/', views.me_view, name='me'),
    path('change-password/', views.change_password_view, name='change_password'),
    path('create-elder/', views.create_elder_view, name='create_elder'),
]