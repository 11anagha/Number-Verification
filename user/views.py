import requests

from django.shortcuts import render, redirect
from .forms import LoginForm, NumberForm, RegistrationForm
from django.contrib import messages
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from user.models import ArmstrongNumber, CustomUser
from .serializers import RegistrationSerializer, LoginSerializer, ArmstrongSerializer, UserWithArmstrongNumbersSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated, AllowAny



# -------------------------------------------------------------------------------------------------------------------------
# API Views
# -------------------------------------------------------------------------------------------------------------------------
class RegisterAPIView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = RegistrationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {"message": "Registration successful. You can now log in with your credentials."},
                status=status.HTTP_201_CREATED,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    


class LoginAPIView(APIView):
    permission_classes = []

    def post(self, request, *args, **kwargs):
        serializer = LoginSerializer(data=request.data, context={"request": request})
        serializer.is_valid(raise_exception=True)

        user = serializer.validated_data["user"]

        # Generate JWT tokens
        refresh = RefreshToken.for_user(user)

        return Response(
            {
                "refresh": str(refresh),
                "access": str(refresh.access_token),
                "user": {
                    "id": user.id,
                    "email": user.email,
                },
            },
            status=status.HTTP_200_OK,
        )



def is_armstrong(num: int) -> bool:
    """Check if a number is an Armstrong number."""
    digits = str(num)
    power = len(digits)
    return sum(int(d) ** power for d in digits) == num


class VerifyNumberAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        serializer = ArmstrongSerializer(data=request.data)
        if serializer.is_valid():
            number = serializer.validated_data["number"]
            armstrong = is_armstrong(number)

            response_data = {
                "number": number,
                "is_armstrong": armstrong,
            }

            if armstrong:
                response_data["message"] = f"{number} is an Armstrong number ✅"

                # Save only if requested
                if request.data.get("save"):
                    ArmstrongNumber.objects.create(user=request.user, number=number)
                    response_data["saved"] = True
                    response_data["message"] += " (saved)"
                else:
                    response_data["saved"] = False
            else:
                response_data["message"] = f"{number} is not an Armstrong number ❌"
                response_data["saved"] = False

            return Response(response_data, status=status.HTTP_200_OK)

        return Response(
            {
                "is_armstrong": False,
                "errors": serializer.errors,
            },
            status=status.HTTP_400_BAD_REQUEST,
        )

    def get(self, request, *args, **kwargs):
        """Retrieve all Armstrong numbers saved by the authenticated user."""
        user_numbers = ArmstrongNumber.objects.filter(user=request.user).values_list("number", flat=True)

        return Response(
            {
                "user": request.user.email,
                "armstrong_numbers": list(user_numbers),
                "count": user_numbers.count(),
            },
            status=status.HTTP_200_OK,
        )


class GetGlobalArmstrongNumbersAPIView(APIView):
    permission_classes = [AllowAny]
    authentication_classes = []

    def get(self, request, *args, **kwargs):
        users = CustomUser.objects.prefetch_related('armstrong_numbers').all()
        serializer = UserWithArmstrongNumbersSerializer(users, many=True)
        return Response({
            "total_users": users.count(),
            "users": serializer.data
        }, status=200)
    

# -------------------------------------------------------------------------------------------------------------------------
# Normal Views
# -------------------------------------------------------------------------------------------------------------------------

API_REGISTER_URL = "http://127.0.0.1:8000/api/register/"

def register_page(request):
    if request.method == "POST":
        form = RegistrationForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            res = requests.post(API_REGISTER_URL, json=data)
            if res.status_code == 201:
                messages.success(request, "✅ Registration successful! Now you can login with your credentials.")
                return redirect("login")
            else:
                errors = res.json()
                for field, msgs in errors.items():
                    for msg in msgs:
                        if field == "non_field_errors":
                            messages.error(request, msg)
                        else:
                            messages.error(request, f"{field.capitalize()}: {msg}")
    else:
        form = RegistrationForm()
    return render(request, "user/register.html", {"form": form})




API_LOGIN_URL = "http://127.0.0.1:8000/api/login/"

def login_page(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            res = requests.post(API_LOGIN_URL, json=form.cleaned_data)
            if res.status_code == 200:
                tokens = res.json()
                request.session["access"] = tokens["access"]
                request.session["refresh"] = tokens["refresh"]
                messages.success(request, "✅ Login successful!")
                return redirect("verify_number")
            else:
                errors = res.json()
                for field, msgs in errors.items():
                    for msg in msgs:
                        if field == "non_field_errors":
                            messages.error(request, msg)
                        else:
                            messages.error(request, f"{field.capitalize()}: {msg}")
    else:
        form = LoginForm()
    return render(request, "user/login.html", {"form": form})




API_VERIFY_URL = "http://127.0.0.1:8000/api/verify-number/"

def verify_number(request):
    access = request.session.get("access")
    if not access:
        messages.error(request, "⚠️ Please login first")
        return redirect("login_page")

    result = None
    form = NumberForm(request.POST or None)

    if request.method == "POST" and form.is_valid():
        headers = {"Authorization": f"Bearer {access}"}
        action = request.POST.get("action")  # detect which button was clicked

        payload = form.cleaned_data
        if action == "save":  # only add save flag when "Save Number" is clicked
            payload["save"] = True

        try:
            res = requests.post(API_VERIFY_URL, json=payload, headers=headers, timeout=5)
            if res.status_code == 200:
                result = res.json()
                if result.get("saved"):
                    messages.success(request, "✅ Number verified and saved!")
                else:
                    messages.info(request, "ℹ️ Number verified (not saved).")
            else:
                result = {"message": "❌ Number is not an Armstrong number"}
        except requests.RequestException as e:
            result = {"message": f"⚠️ API connection error: {str(e)}"}

    # Fetch user’s saved numbers
    user_numbers = {"armstrong_numbers": []}
    headers = {"Authorization": f"Bearer {access}"}
    try:
        res = requests.get(API_VERIFY_URL, headers=headers, timeout=5)
        if res.status_code == 200:
            user_numbers = res.json()
    except requests.RequestException as e:
        messages.error(request, f"⚠️ API connection error: {str(e)}")

    return render(
        request,
        "user/verify_number.html",
        {"form": form, "result": result, "user_numbers": user_numbers},
    )





API_GLOBAL_URL = "http://127.0.0.1:8000/api/global-armstrong-numbers/"

def global_page(request):
    res = requests.get(API_GLOBAL_URL)
    data = res.json() if res.status_code == 200 else {}
    return render(request, "user/global.html", {"data": data})
