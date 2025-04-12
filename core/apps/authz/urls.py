from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', views.UserLoginView.as_view(), name='login'),
    path('logout/', views.user_logout_view, name='logout'),
    path('password-reset/', views.UserPasswordResetView.as_view(), name='password_reset'),
]