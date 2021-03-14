from django.urls import path
from .views import *

app_name = 'aspirasi'

urlpatterns = [
    path('', home, name='home'),
    path('create/', CreateAnAspiration.as_view(), name='create'),
    path('list/', MyList.as_view(), name='my-list'),
    path('my/', check_profile, name='cek'),
    # path('profile/', MyProfile.as_view(), name='show-profile'),
    path('profile/', my_profile, name='show-profile'),
    path('profile/create/', CreateProfile.as_view(), name='create-profile'),
    path('profile/create', CreateProfile.as_view(), name='create-profile-check'),
    path('profile/update/', update_profile, name='update')
]
