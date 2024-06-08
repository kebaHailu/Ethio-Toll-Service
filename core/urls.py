from django.urls import path
from .views import register_driver, CustomLoginView, driver_profile

urlpatterns = [
    path('register-driver/', register_driver, name='register-driver'),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('driver-profile/',driver_profile, name='driver-profile')
]