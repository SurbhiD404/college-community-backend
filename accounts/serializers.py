from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password

User = get_user_model()


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    password2 = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['id', 'email', 'username', 'password', 'password2', 'department', 'batch']

    def validate_email(self, value):
        email = value.lower().strip()
        if not email.endswith('@akgec.ac.in'):
            raise serializers.ValidationError("Please use your official @akgec.ac.in email.")
        if User.objects.filter(email=email).exists():
            raise serializers.ValidationError("User with this email already exists.")
        return email

    def validate(self, data):
        if data['password'] != data['password2']:
            raise serializers.ValidationError({'password': "Passwords do not match."})
        validate_password(data['password'])
        return data

    def create(self, validated_data):
        validated_data.pop('password2', None)
        password = validated_data.pop('password')
        user = User(**validated_data)
        user.set_password(password)
        user.is_email_verified = False
        user.is_active = True
        user.save()
        return user


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email', 'username', 'is_email_verified', 'department', 'batch']

class UserUpdateSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=False)
    confirm_password = serializers.CharField(write_only=True, required=False)

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'confirm_password']

    def validate(self, data):
        email = data.get('email')
        if email and not email.endswith('@akgec.ac.in'):
            raise serializers.ValidationError("Email must be a valid @akgec.ac.in address.")

        password = data.get('password')
        confirm_password = data.get('confirm_password')
        if password or confirm_password:
            if password != confirm_password:
                raise serializers.ValidationError("Passwords do not match.")
            validate_password(password)
        return data

    def update(self, instance, validated_data):
        instance.username = validated_data.get('username', instance.username)
        instance.email = validated_data.get('email', instance.email)

       
        password = validated_data.get('password')
        if password:
            instance.set_password(password)

        instance.save()
        return instance
class LogoutSerializer(serializers.Serializer):
    refresh = serializers.CharField()