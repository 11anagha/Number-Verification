from django.urls import path
from .views import (
    RegisterAPIView, 
    LoginAPIView, 
    VerifyNumberAPIView, 
    GetGlobalArmstrongNumbersAPIView,
    global_page,
    login_page,
    register_page,
    verify_number)


urlpatterns = [
    # -------------------------------------------------------------------------------------------------------------------------
    # API Urls
    # -------------------------------------------------------------------------------------------------------------------------
    path("api/register/", RegisterAPIView.as_view(), name="register_api"),
    path("api/login/", LoginAPIView.as_view(), name="login_api"),
    path("api/verify-number/", VerifyNumberAPIView.as_view(), name="verify_number_api"),
    path("api/get-numbers/", VerifyNumberAPIView.as_view(), name="get_numbers_api"),
    path('api/global-armstrong-numbers/', GetGlobalArmstrongNumbersAPIView.as_view(), name="global_armstrong_numbers_api"),


    # -------------------------------------------------------------------------------------------------------------------------
    # Normal Urls
    # -------------------------------------------------------------------------------------------------------------------------
    path("register/", register_page, name="register"),
    path("login/", login_page, name="login"),
    path("verify_number/", verify_number, name="verify_number"),
    path("", global_page, name="global_page"),
]