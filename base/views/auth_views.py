
from ..utils import email_util
from .. import utils
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse
import jwt
from django.db import transaction
from rest_framework.generics import GenericAPIView
from django.conf import settings
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework.decorators import api_view, permission_classes, parser_classes
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from rest_framework import status

from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from django.contrib.auth.models import User

from django.contrib.auth.hashers import check_password, make_password
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from base.serializers.auth_serializers import *
from base.models import Profile,TutorProfile,TutorVerifictions, StudentProfile


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)

        serializer = UserSerializerWithToken(self.user).data
        for k, v in serializer.items():
            data[k] = v

        return data


class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = UserSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data['user']
            refresh = RefreshToken.for_user(user)
            return Response({
                'access': str(refresh.access_token),
                'refresh': str(refresh)
            }, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_401_UNAUTHORIZED)

    #serializer_class = MyTokenObtainPairSerializer


@api_view(['POST'])
@transaction.atomic()
def tutorRegister(request):
    data = request.data
    first_name = data.get('first_name', '')
    last_name = data.get('last_name', '')
    username = data.get('username', '')
    email = data.get('email', '')
    user_type = data.get('user_type', '')
    password = data.get('password', '')
    image = data.get('image', '')
    bio = data.get('bio', '')

    try:
        if User.objects.filter(email=email).exists():
            return Response({"message": "User already exists"}, status=status.HTTP_400_BAD_REQUEST)

        user = User.objects.create(
            first_name=first_name,
            last_name=last_name,
            username=username,
            email=email,
            password=make_password(password)
        )

        if Profile.objects.filter(email=email).exists():
            return Response({"message": "Profile already exists"}, status=status.HTTP_400_BAD_REQUEST)

        profile = Profile.objects.create(
            user=user,
            full_name=username,
            email=email,
            user_type=user_type,
            image=image,
            bio=bio,
        )

        # TutorProfile instance
        if user_type == 'tutor':
            tutor = TutorProfile.objects.create(
                profile=profile,
                grades=data.get('grades'),
                sessionRate=data.get('sessionRate'),
                availability_days=data.get('availability_days', []),
                available_time=data.get('available_time', [])
            )

            # TutorVerification instance
            tutor_verification = TutorVerifictions.objects.create(
                profile=profile,
                means_of_identity=data.get('means_of_identity'),
                document=data.get('document')
            )

        serializer = UserSerializerWithToken(user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    except ValidationError as e:
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



@api_view(['POST'])
@transaction.atomic
def studentRegister(request):
    data = request.data
    first_name = data.get('first_name')
    last_name = data.get('last_name')
    username = data.get('username')
    email = data.get('email')
    user_type = data.get('user_type')
    password = data.get('password')
    image = data.get('image')
    bio = data.get('bio')


    try:

        user = User.objects.create(
            first_name=first_name,
            last_name=last_name,
            username=username,
            email=email,
            password=make_password(password)
        )


        profile = Profile.objects.create(
            user=user,
            full_name=username,
            email=email,
            user_type=user_type,
            image=image,
            bio=bio,

        )

        # Student Profile
        if user_type == 'student':
            StudentProfile.objects.create(
                profile=profile,
                grade_level = data.get('grade_level'),
                preferred_subjects= data.get('preferred_subjects'),
                learning_goal=data.get('learning_goal'),
                timezone = data.get('timezone'),
                country= data.get('country'),

            )

        # current_site = get_current_site(request).domain
        # relative_link = reverse('email-verify')
        # protocol = request.scheme
        # token = RefreshToken.for_user(email)
        # absurl = protocol+'://'+current_site+relative_link+"?token="+str(token)
        # email_body = 'Hi '+ user['username'] + \
        #      ' Use the link below to verify your email \n' + absurl
        # data = {'email_body': email_body, 'to_email': user['email'],
        #          'email_subject': 'Verify your email'}

        # email_util.Util.send_email(data=data)

        #Return success response
        serializer = UserSerializerWithToken(user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    except ValidationError as e:
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



@api_view(['POST'])
@permission_classes([IsAuthenticated])
def UserChangePassword(request):
    try:
        data = request.data
        user = request.user

        old_password = data['old_password']
        new_password = data['new_password']

        # Verify old password
        if not check_password(old_password, user.password):
            return Response({"detail": "Old password is incorrect"}, status=status.HTTP_400_BAD_REQUEST)

        # Validate new password
        try:
            validate_password(new_password, user)
        except ValidationError as e:
            return Response({"detail": e.messages}, status=status.HTTP_400_BAD_REQUEST)

        # Set new password
        user.password = make_password(new_password)
        user.save()

        return Response({"message": "Password reset successful"}, status=status.HTTP_200_OK)
    except User.DoesNotExist:
        return Response({"detail": "User does not exist"}, status=status.HTTP_404_NOT_FOUND)


class VerifyEmailView(GenericAPIView):
    serializer_class = EmailVerificationSerializer

    token_param_config = openapi.Parameter(
        'token', in_=openapi.IN_QUERY, description='Description', type=openapi.TYPE_STRING)

    @swagger_auto_schema(manual_parameters=[token_param_config])
    def get(self, request):
        token = request.GET.get('token')
        try:
            payload = jwt.decode(token, options={"verify_signature": False})
            user = User.objects.get(id=payload['user_id'])
            profile = Profile.objects.get(user=user)
            if not profile.is_verified:
                profile.is_verified = True
                profile.save()
            return Response({'email': 'Successfully activated'}, status=status.HTTP_200_OK)
        except jwt.ExpiredSignatureError as identifier:
            return Response({'error': 'Activation Expired'}, status=status.HTTP_400_BAD_REQUEST)
        except jwt.exceptions.DecodeError as identifier:
            return Response({'error': 'Invalid token'}, status=status.HTTP_400_BAD_REQUEST)