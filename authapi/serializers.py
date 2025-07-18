from functools import cache
import requests

from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model

from rest_framework import serializers

from authapi.validators import password_validation, validate_email
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_decode
from django.utils.encoding import force_str


# Aditya changes

from rest_framework import serializers
from django.contrib.auth import get_user_model
from authapi.validators import validate_email, password_validation
from authapi.models import PasswordResetOTP

User = get_user_model()


class UserListSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = User 
        fields = ['username', 'first_name', 'last_name', 'country', 'user_type']


class UserCreateSerializer(serializers.ModelSerializer):

    password = serializers.CharField(max_length=20, write_only=True)
    confirm_password = serializers.CharField(max_length=20, write_only=True)
    
    class Meta:
        model = User 
        fields = ['username', 'first_name', 'last_name', 'country', 'user_type', 'password', 'confirm_password']


    def validate_username(self, email):
        if not validate_email(email):
            raise ValidationError('Email is not Valid')
        return email
    
    def validate_password(self, password):
        if not password_validation(password):
            raise ValidationError("Password not Valid")
        
        return password
    
    def validate_confirm_password(self, confirm_password):
        if not password_validation(confirm_password):
            raise ValidationError("Confirm Password not Valid")
        
        return confirm_password
    

    def validate(self, attrs):
        if attrs.get('password') != attrs.get('confirm_password'):
            raise ValidationError('password not matched.')
        return super().validate(attrs)
    
    def create(self, validated_data):
        validated_data.pop('confirm_password')
        instance = User(**validated_data)
        instance.set_password(validated_data.get('password'))
        instance.save()
        try:
            response = requests.get(f'http://localhost:5000/mail/{instance.username}/{instance.first_name}')
            print(response)
        except:
            pass
        return instance
    
    
    
    
# serializers.py


# User = get_user_model()

class CombinedForgotResetPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField()
    otp = serializers.CharField(required=False)
    new_password = serializers.CharField(write_only=True, required=False,style={'input_type': 'password'})
    confirm_password = serializers.CharField(write_only=True, required=False,style={'input_type': 'password'})

    def validate(self, attrs):
        email = attrs.get("email")
        otp = attrs.get("otp")
        new_password = attrs.get("new_password")
        confirm_password = attrs.get("confirm_password")

        
        if not validate_email(email):
            raise serializers.ValidationError({"email": "Invalid email format"})

        try:
            user = User.objects.get(username=email)
        except User.DoesNotExist:
            raise serializers.ValidationError({"email": "Email does not exist"})

        
        if not otp and not new_password and not confirm_password:
            attrs['user'] = user  
            return attrs

        
        try:
            otp_obj = PasswordResetOTP.objects.filter(user__username=email).latest("created_at")
        except PasswordResetOTP.DoesNotExist:
            raise serializers.ValidationError({"otp": "OTP not found"})

        if otp_obj.otp != otp:
            raise serializers.ValidationError({"otp": "Invalid OTP"})

        if otp_obj.is_expired():
            raise serializers.ValidationError({"otp": "OTP has expired"})

        if new_password != confirm_password:
            raise serializers.ValidationError({"password": "Passwords do not match"})
        

        if not password_validation(new_password):
            raise serializers.ValidationError({"password": "Weak password"})

        attrs['user'] = user  # Attach user for view
        return attrs
    
    
class ResetPasswordView(serializers.Serializer):
    email = serializers.EmailField()
    current_password=serializers.CharField(write_only=True,style={'input_type':'password'})
    new_password = serializers.CharField(write_only=True,style={'input_type': 'password'})
    confirm_password = serializers.CharField(write_only=True,style={'input_type': 'password'})
    
    def validate(self, attrs):
        email = attrs.get("email")
        current_password=attrs.get("current_password")
        new_password=attrs.get("new_password")
        confirm_password=attrs.get("confirm_password")
        
        
        if not validate_email(email):
            raise serializers.ValidationError({"email": "Invalid email format"})

        try:
            user = User.objects.get(username=email)
        except User.DoesNotExist:
            raise serializers.ValidationError({"email": "Email does not exist"})
        
        if new_password != confirm_password:
            raise serializers.ValidationError({"password": "Passwords do not match"})
        
        if new_password==current_password:
            raise serializers.ValidationError({"newpassword and currentpassword cannot be same"})

        if not password_validation(new_password):
            raise serializers.ValidationError({"password": "Weak password"})
        
        if not user.check_password(current_password):
            raise serializers.ValidationError({"password": "Current password is incorrect"})

        
        attrs['user'] = user  
        return attrs
        
        
        
        
    
    


    
    
    



