from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken

User = get_user_model()


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=9)
    password2 = serializers.CharField(write_only=True, min_length=9)

    class Meta:
        model = User
        fields = ["username", "email", "password", "password2"]

    def validate(self, attrs):
        if attrs["password"] != attrs["password2"]:
            # shape it for the confirm field so FE can map it inline
            raise serializers.ValidationError({"password2": ["Passwords do not match."]})
        return attrs

    def create(self, validated_data):
        # don’t pass password/password2 through **kwargs; set it explicitly
        password = validated_data.pop("password")
        validated_data.pop("password2", None)

        # create the user
        user = User.objects.create_user(**validated_data)
        user.set_password(password)
        user.save()

        # include JWTs so the FE can auto-login after registration
        refresh = RefreshToken.for_user(user)
        return {
            "user": {"username": user.username, "email": user.email},
            "access": str(refresh.access_token),  # type: ignore[attr-defined]
            "refresh": str(refresh),
        }
