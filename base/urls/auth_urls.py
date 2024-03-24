from django.urls import path
from base.views import auth_views as views


urlpatterns = [
        path('login/',views.MyTokenObtainPairView.as_view(),
         name='token_obtain_pair'),
        path('register_tutor/', views.tutorRegister, name="register-user"),
        path('register_student/', views.studentRegister, name="register-user"),
        path('changepassword/', views.UserChangePassword, name="change"),
        path('email-verify', views.VerifyEmailView.as_view(), name='email-verify'),

]
