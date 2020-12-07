from django.urls import path

from registrator.views import RegisterStudentView, RegisterTeacherView, logout_user, login_user

urlpatterns = [
    path('student/', RegisterStudentView.as_view(), name='register-student'),
    path('teacher/', RegisterTeacherView.as_view(), name='register-teacher'),
    path('login/', login_user, name='login'),
    path('logout/', logout_user, name='logout')
]

