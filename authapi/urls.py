from django.urls import path 
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenVerifyView

from authapi.views import (UserListAPIView, UserCreateAPIView,CombinedForgotResetPasswordAPIView,ResetPasswordApiView)

app_name = 'authapi'

urlpatterns = [
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('token/verify/', TokenVerifyView.as_view(), name='token_verify'),

    path('list/user/', UserListAPIView.as_view(), name='list-user'),
    path('create/user/', UserCreateAPIView.as_view(), name='create-user'),
    path('forgot-password/', CombinedForgotResetPasswordAPIView.as_view(), name='forgot-password'),
    path('reset-password/', ResetPasswordApiView.as_view(), name='reset-password'),
    
]

