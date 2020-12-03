from django.urls import path

from registrator.views import RegisterStudentView, RegisterTeacherView

urlpatterns = [
    path('student/', RegisterStudentView.as_view(), name='register-student'),
    path('teacher/', RegisterTeacherView.as_view(), name='register-teacher'),
]
