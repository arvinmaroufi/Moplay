from django.urls import path
from . import views


app_name = 'dashboard'

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('notifications/<int:notification_id>/mark-as-read/', views.mark_notification_as_read, name='mark_notification_as_read'),
]
