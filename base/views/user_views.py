
from django.core.mail import send_mail

from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view, permission_classes, parser_classes
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from rest_framework import status
from base.serializers.auth_serializers import ProfileSerializer
from base.models import Profile,TutorProfile,StudentProfile
from base.serializers.tutor_serializers import TutorProfileSerializer
from base.serializers.students_serializer import StudentProfileSerializer

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def profile(request):
    try:
        profile = request.user.profile
        serializer = ProfileSerializer(profile, many=False)
        return Response(serializer.data)
    except Profile.DoesNotExist:
        return Response({'error': 'Profile not found'}, status=status.HTTP_404_NOT_FOUND)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def getTutorProfile(request):
    profile = request.user.profile

    if profile.usertype == 'tutor':
        tutor = TutorProfile.objects.get(profile=profile)
        serializer = TutorProfileSerializer(tutor, many=False)
        return Response(serializer.data)
    else:
        return Response({"message": "You have no permission to access this page"}, status=status.HTTP_404_NOT_FOUND)
    

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def getStudentProfile(request):
    profile = request.user.profile

    if profile.user_type == 'student':
        student = StudentProfile.objects.get(profile=profile)
        serializer = StudentProfileSerializer(student, many=False)
        return Response(serializer.data)
    else:
        return Response({"message": "You have no permission to access this page"}, status=status.HTTP_404_NOT_FOUND)
    



@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def editProfile(request):
    user = request.user
    data = request.data
    first_name = data.get('first_name')
    last_name = data.get('last_name')
    bio = data.get('bio')

    try:
        profile = user.profile
        

    except Profile.DoesNotExist:
        return Response({'error': 'Profile not found'}, status=status.HTTP_404_NOT_FOUND)


    user.username = data.get('full_name',user.username)
    user.email = data.get('email', user.email)
    profile.full_name= user.username
    profile.first_name = user.first_name
    profile.last_name = user.last_name
    profile.bio = bio
    profile.email =  user.email
    profile.phone = data.get('phone', profile.phone)
    user.save()
    profile.save()
    return Response({'message': 'Profile update successful'})


@api_view(['PUT'])
def uploadProfilePhoto(request):
    data = request.data
    profile_id=data['userId']
    profile =  Profile.objects.get(_id=profile_id)
    profile.image = request.FILES.get('image')
    profile.save()
    return Response("image was uploaded")
