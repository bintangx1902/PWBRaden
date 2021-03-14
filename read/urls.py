from django.urls import path
from .views import *

app_name = 'read'

urlpatterns = [
    path('', AllAspirations.as_view(), name='list'),
    path('update/<int:pk>/', read_view, name='marked'),
    path('<int:pk>', ReadAspiration.as_view(), name='read'),
    path('<int:pk>/', ReadAspiration.as_view(), name='read'),
    path('<int:pk>/feedback', CreateFeedback.as_view(), name='feedback'),
    path('<int:pk>/feedback/', CreateFeedback.as_view(), name='feedback'),
]

