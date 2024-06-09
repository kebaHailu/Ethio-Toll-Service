from django.urls import path
from .views import register_driver, CustomLoginView, driver_profile, check_card , check_uid

urlpatterns = [
    path('', register_driver, name='register-driver'),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('profile',driver_profile, name='driver-profile'),
    path('check',check_card, name='check'),
    path('check_uid/',check_uid, name='check-uid')
]