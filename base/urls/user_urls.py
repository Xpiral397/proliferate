from django.urls import path
from base.views.user_views import (
    profile,
    getTutorProfile,
    getStudentProfile,
    editProfile,
    uploadProfilePhoto,
)

urlpatterns = [
    path('profile/', profile, name='profile'),
    path('get-tutor-profile/', getTutorProfile, name='get-tutor-profile'),
    path('get-student-profile/', getStudentProfile, name='get-student-profile'),
    path('edit-profile/', editProfile, name='edit-profile'),
    path('upload-profile-photo/', uploadProfilePhoto, name='upload-profile-photo'),
]
