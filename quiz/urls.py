from django.urls import path

from quiz.views import render_home, QuizCreateView, StudentDetailView, TeacherDetailView, question_create_view, \
    QuizDetailView, QuestionDetailView, answer_create_view

urlpatterns = [
    path('', render_home, name='quiz-home'),
    path('student/<int:pk>/', StudentDetailView.as_view(), name='student-detail'),
    path('teacher/<int:pk>/', TeacherDetailView.as_view(), name='teacher-detail'),
    path('quiz/create/', QuizCreateView.as_view(), name='quiz-create'),
    path('quiz/detail/<int:pk>/', QuizDetailView.as_view(), name='quiz-detail'),
    path('quiz/delete/<int:pk>/', name='quiz-delete'),
    path('quiz/detail/<int:pk>/question/<int:id>/', QuestionDetailView.as_view(), name='question-detail'),
    path('quiz/edit/<int:pk>/question/add/', question_create_view, name='question-create'),
    path('quiz/edit/<int:quiz_id>/question/<int:question_id>/answer/create/', answer_create_view, name='answer-create'),
    #path('quiz/edit/<int:pk>/question/edit/<int:pk>/', question_edit_view, name='question-create'),
]
