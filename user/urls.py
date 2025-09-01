from django.urls import path
from .views import (
    RegisterAPIView, 
    LoginAPIView, 
    VerifyNumberAPIView, 
    GetGlobalArmstrongNumbersAPIView)


urlpatterns = [
    path("register/", RegisterAPIView.as_view(), name="register"),
    path("login/", LoginAPIView.as_view(), name="login"),
    path("verify-number/", VerifyNumberAPIView.as_view(), name="verify_number"),
    path("get-numbers/", VerifyNumberAPIView.as_view(), name="get_numbers"),
    path('global-armstrong-numbers/', GetGlobalArmstrongNumbersAPIView.as_view(), name="global_armstrong_numbers"),
]