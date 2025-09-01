from django.shortcuts import render, redirect
from .forms import RegisterationForm
from django.contrib import messages

# -------------------------------------------------------------------------------------------------------------------------
# API Views
# -------------------------------------------------------------------------------------------------------------------------
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from user.models import ArmstrongNumber, CustomUser
from .serializers import RegistrationSerializer, LoginSerializer, ArmstrongSerializer, UserWithArmstrongNumbersSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated, AllowAny

class RegisterAPIView(APIView):
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



class VerifyNumberAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        serializer = ArmstrongSerializer(data=request.data)
        if serializer.is_valid():
            number = serializer.validated_data["number"]

            # Save Armstrong number for the authenticated user
            ArmstrongNumber.objects.create(user=request.user, number=number)

            return Response(
                {
                    "number": number,
                    "is_armstrong": True,
                    "message": "The number is an Armstrong number ✅",
                },
                status=status.HTTP_200_OK,
            )
        return Response(
            {
                "is_armstrong": False,
                "errors": serializer.errors,
            },
            status=status.HTTP_400_BAD_REQUEST,
        )
    

    def get(self, request, *args, **kwargs):
        # Retrieve all Armstrong numbers for the authenticated user
        user_numbers = ArmstrongNumber.objects.filter(user=request.user)
        serializer = ArmstrongSerializer(user_numbers, many=True)
        return Response(
            {
                "user": request.user.email,
                "armstrong_numbers": serializer.data,
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