
from django.core.mail import send_mail

from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view, permission_classes, parser_classes
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from rest_framework import status
from django.core.paginator import Paginator,PageNotAnInteger,EmptyPage
from base.serializers.auth_serializers import ProfileSerializer
from base.models import Profile,TutorProfile,Class,Assignment,Subject,classSchedule,StudentProfile,ClassMessage
from base.serializers.tutor_serializers import TutorProfileSerializer,ClassSerializer,AssignmentSerializer,classScheduleSerializer, ClassMessageSerializer
from django.db.models import Q



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


#find tutors
@api_view(['GET'])
def  findTutors(request):
    query = request.query_params.get('keyword')
    if query == None:
        query= ''
    tutors = TutorProfile.objects.filter(
        full_name__icontains=query).order_by('-createdAt')

    page =request.query_params.get('page')
    paginator = Paginator(tutors, 10)

    try:
        tutors = paginator.page(page)
    except PageNotAnInteger:
        tutors = paginator.page(1)
    except EmptyPage:
        tutors = paginator.page(paginator.num_pages)

    if page  == None:
        page =1

    page = int(page)


    serializer = TutorProfileSerializer(tutors, many=True)
    return  Response({'tutors':serializer.data, 'page': page, 'pages': paginator.num_pages})



@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_class(request):
    serializer = ClassSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def update_class(request, pk):
    class_instance = get_object_or_404(Class, pk=pk)
    serializer = ClassSerializer(class_instance, data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_class(request, pk):
    class_instance = get_object_or_404(Class, pk=pk)
    class_instance.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def addStudentToClass(request,id):
    currentclass =get_object_or_404(Class,id=id)
    data = request.data
    email = data.get('email')

    student = Profile.objects.get(email=email)
    currentclass.students.add(student)
    currentclass.save()



@api_view(['GET'])
@permission_classes([IsAuthenticated])
def getClassById(request,pk):
    classid =Class.objects.get(pk=pk)
    serializer = ClassSerializer(classid,many=False)
    return Response(serializer.data) 



@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_class_students(request, class_id):
    try:
        classid= Class.objects.get(id=class_id)
        students= classid.students.all()
        serializer = ProfileSerializer(students, many=True)
        return Response(serializer.data)
    except Class.DoesNotExist:
        return Response({'error': 'class not found'}, status=404)
    

     
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_messages(request, class_id):
    
    messages = ClassMessage.objects.filter(class_id=class_id)

   
    serializer = ClassMessageSerializer(messages,many=True  )

    return  Response(serializer.data)



@api_view(['POST'])
@permission_classes([IsAuthenticated])
def send_message(request, class_id):
    data = request.data
    profile = request.user.profile
    
    

    file = request.FILES.get('file')

    message = ClassMessage.objects.create(
        sender = profile,
        classid = Class.objects.get(_id=class_id),
        
        content = data['content'],
        file =file

    )
    serializer = ClassMessageSerializer(message)
    return Response('Messsage sent')


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def getMyClasses(request):
    profile = request.user.profile
    classes = Class.objects.filter(tutor=profile)
    serializer = ClassSerializer(classes, many=True)
    return Response(serializer.data)

#assignments

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def getMyAssignments(request):
    profile = request.user.profile
    assignments = Assignment.objects.filter(tutor=profile)
    serializer = ClassSerializer(assignments, many=True)
    return Response(serializer.data)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_assignment(request):
    serializer = AssignmentSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def update_assignment(request, pk):
    assignment_instance = get_object_or_404(Assignment, pk=pk)
    serializer = AssignmentSerializer(assignment_instance, data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_assignment(request, pk):
    assignment_instance = get_object_or_404(Assignment, pk=pk)
    assignment_instance.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)