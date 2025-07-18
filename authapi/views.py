from django.shortcuts import render
from django.contrib.auth import get_user_model

from rest_framework.response import Response
from rest_framework.generics import ListAPIView, CreateAPIView
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny
from rest_framework_simplejwt.authentication import JWTAuthentication

from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.core.mail import send_mail
from django.contrib.auth.tokens import default_token_generator
from rest_framework.views import APIView


from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import CombinedForgotResetPasswordSerializer,ResetPasswordView
from django.contrib.auth import get_user_model
import random
from .models import PasswordResetOTP



from authapi.serializers import (UserListSerializer, UserCreateSerializer)

User = get_user_model()


class UserListAPIView(ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserListSerializer
    permission_classes = [IsAuthenticated]


class UserCreateAPIView(CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserCreateSerializer
    permission_classes = [AllowAny]
    
    
class CombinedForgotResetPasswordAPIView(GenericAPIView):
    serializer_class = CombinedForgotResetPasswordSerializer  

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)  
        if serializer.is_valid():
            email = serializer.validated_data.get("email")
            otp = serializer.validated_data.get("otp")
            new_password = serializer.validated_data.get("new_password")
            user = serializer.validated_data.get("user")

            if not otp:
                otp_code = str(random.randint(100000, 999999))
                PasswordResetOTP.objects.create(user=user, otp=otp_code)
                print(f"[DEBUG] OTP for {email}: {otp_code}")
                return Response({"message": "OTP sent to your email"}, status=200)

            
            user.set_password(new_password)
            user.save()
            PasswordResetOTP.objects.filter(user=user).delete()
            return Response({"message": "Password has been reset"}, status=200)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    
class ResetPasswordApiView(GenericAPIView):
    serializer_class = ResetPasswordView
    
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)  
        if serializer.is_valid():
            email = serializer.validated_data.get("email")
            current_password = serializer.validated_data.get("current_password")
            new_password = serializer.validated_data.get("new_password")
            confirm_password = serializer.validated_data.get("confirm_password")
            
            try:
                    user = User.objects.get(username=email)  
            except User.DoesNotExist:
                    return Response({"message": "User not found"}, status=404)

            
            if user.check_password(current_password) and new_password == confirm_password:
                user.set_password(new_password)
                user.save()
                return Response({"message": "Password has been reset"}, status=200)
            else:
                return Response({"message": "Current password incorrect or new passwords don't match"}, status=400)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

            
        
            
            
    
