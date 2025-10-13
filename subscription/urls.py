from django.urls import path
from . import views


app_name = 'subscription'

urlpatterns = [
    path('plans/', views.subscription_plans, name='plans'),
]
