from django.contrib.auth import get_user_model
from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth import authenticate

from user.models import CustomUser

User = get_user_model()

class RegistrationSerializer(serializers.ModelSerializer):
    password1 = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ["email", "password1", "password2"]

    def validate(self, attrs):
        if attrs["password1"] != attrs["password2"]:
            raise serializers.ValidationError({"password": "Passwords do not match."})
        return attrs

    def create(self, validated_data):
        user = User.objects.create_user(
            email=validated_data["email"],
            password=validated_data["password1"],
        )
        return user
    


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    password = serializers.CharField(
        write_only=True,
        required=True,
        style={"input_type": "password"}
    )

    def validate(self, attrs):
        email = attrs.get("email")
        password = attrs.get("password")

        if not email or not password:
            raise serializers.ValidationError(
                {"detail": "Both email and password are required."}
            )

        user = authenticate(request=self.context.get("request"), email=email, password=password)

        if not user:
            raise serializers.ValidationError(
                {"detail": "Invalid email or password."}
            )

        if not user.is_active:
            raise serializers.ValidationError(
                {"detail": "This account is disabled."}
            )

        attrs["user"] = user
        return attrs



class ArmstrongSerializer(serializers.Serializer):
    number = serializers.IntegerField(required=True, min_value=0)

    def validate_number(self, value):
        num_str = str(value)
        power = len(num_str)
        total = sum(int(digit) ** power for digit in num_str)

        if value == total:
            return value
        raise serializers.ValidationError("This is not an Armstrong number.")



class UserWithArmstrongNumbersSerializer(serializers.ModelSerializer):
    armstrong_numbers = ArmstrongSerializer(many=True, read_only=True)

    class Meta:
        model = CustomUser
        fields = ["id", "email", "armstrong_numbers"]