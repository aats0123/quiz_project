from django.urls import path

from registrator.views import RegisterStudentView, RegisterTeacherView, logout_user, login_user, \
    SchoolClassRegisterView

urlpatterns = [
    path('student/', RegisterStudentView.as_view(), name='register-student'),
    # path('student/edit/<int:pk>', student_edit_view, name='student-edit'),
    path('teacher/', RegisterTeacherView.as_view(), name='register-teacher'),
    path('teacher/<int:pk>/class-register/', SchoolClassRegisterView.as_view(), name='class-register'),
    path('login/', login_user, name='login'),
    path('logout/', logout_user, name='logout')
]

