from django.urls import path
from . import views


app_name = 'subscription'

urlpatterns = [
    path('plans/', views.subscription_plans, name='plans'),
    path('select/<int:plan_id>/', views.select_plan, name='select_plan'),
    path('subscription/<int:subscription_id>/', views.subscription_detail, name='subscription_detail'),
    path('my-subscriptions/', views.user_subscriptions, name='user_subscriptions'),
]
