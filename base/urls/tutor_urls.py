from django.urls import path
from ..views import *
from base.views.tutor_views import (
    getTutorProfile,
    findTutors,
    create_class,
    update_class,
    delete_class,
    addStudentToClass,
    getClassById,
    get_class_students,
    get_messages,
    send_message,
    getMyClasses,
    getMyAssignments,
    create_assignment,
    update_assignment,
    delete_assignment,
)

urlpatterns = [
    path('get-tutor-profile/', getTutorProfile, name='get-tutor-profile'),
    path('find-tutors/', findTutors, name='find-tutors'),
    path('create-class/', create_class, name='create-class'),
    path('update-class/<int:pk>/', update_class, name='update-class'),
    path('delete-class/<int:pk>/', delete_class, name='delete-class'),
    path('add-student-to-class/<int:id>/', addStudentToClass, name='add-student-to-class'),
    path('get-class-by-id/<int:pk>/', getClassById, name='get-class-by-id'),
    path('get-class-students/<int:class_id>/', get_class_students, name='get-class-students'),
    path('get-messages/<int:class_id>/', get_messages, name='get-messages'),
    path('send-message/<int:class_id>/', send_message, name='send-message'),
    path('get-my-classes/', getMyClasses, name='get-my-classes'),
    path('get-my-assignments/', getMyAssignments, name='get-my-assignments'),
    path('create-assignment/', create_assignment, name='create-assignment'),
    path('update-assignment/<int:pk>/', update_assignment, name='update-assignment'),
    path('delete-assignment/<int:pk>/', delete_assignment, name='delete-assignment'),
]
