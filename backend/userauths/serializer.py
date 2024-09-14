from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.tokens import Token

from userauths.models import Profile, User


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    """
    Custom token serializer to include additional user information in the token.
    """

    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        # Add custom claims
        token['full_name'] = user.full_name
        token['email'] = user.email
        token['username'] = user.username
        try:
            token['vendor_id'] = user.vendor.id
        except AttributeError:
            token['vendor_id'] = None

        return token


class RegisterSerializer(serializers.ModelSerializer):
    """
    Serializer for user registration.
    """
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ['full_name', 'email', 'phone', 'password', 'password2']

    def validate(self, attrs):
        """
        Validate that the two password fields match.
        """
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Password fields didn't match."})
        return attrs

    def create(self, validated_data):
        """
        Create a new user with the provided validated data.
        """
        user = User.objects.create(
            full_name=validated_data['full_name'],
            email=validated_data['email'],
            phone=validated_data['phone'],
        )

        # Set the username to be the part of the email before the '@'
        email_user, _ = user.email.split('@')
        user.username = email_user
        user.set_password(validated_data['password'])
        user.save()

        return user


class UserSerializer(serializers.ModelSerializer):
    """
    Serializer for the User model.
    """

    class Meta:
        model = User
        fields = "__all__"


class ProfileSerializer(serializers.ModelSerializer):
    """
    Serializer for the Profile model.
    """

    class Meta:
        model = Profile
        fields = "__all__"

    def to_representation(self, instance):
        """
        Customize the representation of the Profile model to include user data.
        """
        response = super().to_representation(instance)
        response['user'] = UserSerializer(instance.user).data
        return response