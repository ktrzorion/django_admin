from rest_framework import serializers
from rest_framework.serializers import ValidationError
from .models import MyUser
from rest_framework_simplejwt.tokens import RefreshToken, TokenError
from django.utils.encoding import smart_str, force_bytes, DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.contrib.auth.tokens import PasswordResetTokenGenerator

class UserRegistrationSerializer(serializers.ModelSerializer):
    re_password = serializers.CharField(style={'input_type': 'password'}, write_only=True)
    class Meta:
        model = MyUser
        fields = ['email', 'name', 'password', 're_password', 'tc']
        extra_kwargs = {
            'password' : {'write_only':True}
        }

    def validate(self, attrs):
        password = attrs.get('password')
        re_password = attrs.get('re_password')

        if password != re_password:
            raise serializers.ValidationError('Password & Confirm Password does not match!')
        return attrs
    
    def create(self, validate_data):
        return MyUser.objects.create_user(**validate_data)
    
class UserLoginSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(max_length=255)
    class Meta:
        model = MyUser
        fields = ['email', 'password']

class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = MyUser
        fields = ['id', 'email', 'name']

class UserLogoutSerializer(serializers.ModelSerializer):
    refresh = serializers.CharField()

    default_error_messages = {
        'bad_token':('Token is expired or invalid')
    }

    def save(self, **kwargs):
        try:
            RefreshToken(self.token).blacklist()

        except TokenError:
            self.fail('bad_token')

class ChangePasswordSerializer(serializers.Serializer):
    new_password = serializers.CharField(max_length=255, style={'input_type': 'password'}, write_only=True)
    re_password = serializers.CharField(max_length=255, style={'input_type': 'password'}, write_only=True)

    class Meta:
        fields = ['new_password', 're_password']

    def validate(self, attrs):
        new_password = attrs.get('new_password')
        re_password = attrs.get('re_password')

        if new_password != re_password:
            raise serializers.ValidationError("Password does't match!")
        user = self.context.get('user')
        user.set_password(new_password)
        user.save()
        return (attrs)
    
class SendPasswordResetEmailSerializer(serializers.Serializer):
    email = serializers.EmailField(max_length=255)
    class Meta:
        fields = ['email']

    def validate(self, attrs):
        email = attrs.get('email')
        if MyUser.objects.filter(email=email).exists():
            user = MyUser.objects.get(email=email)
            uid = urlsafe_base64_encode(force_bytes(user.id))
            print('Encoded UID', uid)
            token = PasswordResetTokenGenerator().make_token(user)
            print('Password Token', token)
            link = 'http://localhost:3000/api/reset/'+uid+'/'+token
            print('Password Reset Link', link)
            body = 'Click Following To Reset Your Password' + link
            data = {
                'subject':'Reset Your Password',
                'body':body,
                'to_email':user.email
            }
            return attrs
        else:
            raise ValidationError('You are not a Registered User')
        return super().validate(attrs)
    
class UserPasswordResetSerializer(serializers.Serializer):
    new_password = serializers.CharField(max_length=255, style={'input_type': 'password'}, write_only=True)
    re_password = serializers.CharField(max_length=255, style={'input_type': 'password'}, write_only=True)

    class Meta:
        fields = ['new_password', 're_password']

    def validate(self, attrs):
        try:
            new_password = serializers.CharField(max_length=255)
            re_password = serializers.CharField(max_length=255)

            uid = self.context.get(uid)
            token = self.context.get(token)

            if new_password != re_password:
                raise serializers.ValidationError("Password Dosen't Match!")

            id = smart_str(urlsafe_base64_decode(uid))
            user = MyUser.objects.filter(id=id)

            if not PasswordResetTokenGenerator().check_token(user, token):
                raise ValidationError('Token is not Valid or Expired!')
            user.set_password(new_password)
            user.save()
            return attrs
        except DjangoUnicodeDecodeError as identifier:
            PasswordResetTokenGenerator().check_token(user, token)
            raise ValidationError('Token is not Valid or Expired!')