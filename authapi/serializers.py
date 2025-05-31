from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model

from rest_framework import serializers

from authapi.validators import password_validation, validate_email

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
        return instance

