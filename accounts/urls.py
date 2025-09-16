from django.urls import path
from . import views


app_name = 'accounts'

urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', views.login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('verify-code/', views.verify_code, name='verify_code'),
    path('resend-code/', views.resend_verification_code, name='resend_code'),
]
