from rest_framework.response import Response
from rest_framework import status
from rest_framework import serializers
from django.contrib.auth import authenticate
from rest_framework.views import APIView
from .serializers import UserRegistrationSerializer, UserLoginSerializer, UserProfileSerializer, UserLogoutSerializer, ChangePasswordSerializer
from authapp.renderers import UserRenderer
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework_simplejwt.tokens import RefreshToken

from authapp import serializers
# from authsys.auth import serializers

def get_tokens(user):
    refresh = RefreshToken.for_user(user)

    return {
        'refresh' : str(refresh),
        'access' : str(refresh.access_token),
    }

class UserRegistrationView(APIView):
    permission_classes = [AllowAny]
    renderer_classes = [UserRenderer]
    def post(self, request, format=None):
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            user = serializer.save()
            return Response({'msg':'Registration Successful'},
                            status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class UserLoginView(APIView):
    renderer_classes = [UserRenderer]
    def post(self, request, format=None):
        serializer = UserLoginSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            email = serializer.data.get('email')
            password = serializer.data.get('password')

            user = authenticate(email=email, password=password)

            if user is not None:
                token = get_tokens(user)
                return Response({'token' : token, 'msg':'Login Successful'}, status=status.HTTP_200_OK)
                # return Response({'msg' : 'Login Success'}, status=status.HTTP_200_OK)
            else:
                return Response({'errors':{'non_field_error':['Email or Password is not valid!']}}, status=status.HTTP_404_NOT_FOUND)
        return Response(serializers.errors, status=status.HTTP_400_BAD_REQUEST)
    
class UserProfileView(APIView):
    renderer_classes = [UserRenderer]
    permission_classes = [IsAuthenticated]
    def get(self, request, format=None):
        serializers = UserProfileSerializer(request.user)
        return Response(serializers.data, status=status.HTTP_200_OK)
    
class UserLogoutView(APIView):
    serializer_class = UserLogoutSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request, format=None):
        serializers = UserLogoutSerializer(data=request.data)
        serializers.is_valid(raise_exception=True)
        serializers.save()

        return Response({'msg':'Log Out Successful'}, status=status.HTTP_204_NO_CONTENT)
    
class UserChangePasswordView(APIView):
    renderer_classes = [UserRenderer]
    permission_classes = [IsAuthenticated]
    
    def post(self, request, format=None):
        serializer = ChangePasswordSerializer(data=request.data, context={'user':request.user})
        if serializers.is_valid(raise_exception=True):
            return Response({'msg' : 'Password Changed Successfully'}, status=status.HTTP_202_ACCEPTED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
# class SendPasswordResetEmailView(APIView):
#     renderer_classes = [UserRenderer]
#     def post(self, request, format=None):
#         serializers = SendPasswordResetEmailSerializer(data=request.data)
        
#         if serializers.is_valid(raise_exception=True):
#             return Response({'msg':'Password Reset Link Sent!'}, status=status.HTTP_200_OK)
        
#         return Response(serializers.errors, staticmethostatus=status.HTTP_400_BAD_REQUEST)
    
class UserPasswordResetView(APIView):
    renderer_classes = [UserRenderer]
    
    def post(self, request, uid, token, format=None):
        serializer = UserPasswordResetSerializer(data=request.data, context = {'uid':uid, 'token':token})

        if serializer.is_valid(raise_exception=True):
            return Response({'msg':'Password Reset Successfully'}, status=status.HTTP_200_OK)
            
        return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)