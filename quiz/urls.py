from django.urls import path

from quiz.views import render_home, QuizCreateView, StudentDetailView, TeacherDetailView, question_create_view, \
    QuizDetailView, QuestionDetailView, answer_create_view, quiz_delete_view, quiz_edit_view, question_delete_view, \
    answer_delete_view, bulk_quiz_create_view, quiz_assign_view, test_take_view, StudentTestsView, \
    AnsweredTestView, assigned_tests_view, QuizSchoolClassView, question_edit_view

urlpatterns = [
    path('', render_home, name='quiz-home'),
    path('student/<int:pk>/', StudentDetailView.as_view(), name='student-detail'),
    path('student/tests/<int:pk>', StudentTestsView.as_view(), name='student-tests'),
    path('student/test/<int:test_id>', test_take_view, name='test-take'),
    path('student/answers/<int:test_id>/', AnsweredTestView.as_view(), name='test-answers'),
    path('teacher/<int:pk>/', TeacherDetailView.as_view(), name='teacher-detail'),
    path('teacher/<int:pk>/assign-quiz', quiz_assign_view, name='quiz-assign'),
    path('teacher/assigned-quizes/', assigned_tests_view, name='assigned-quizzes'),
    path('teacher/quiz/<int:quiz_id>/class/<int:class_id>/', QuizSchoolClassView.as_view(), name='quiz-class'),
    path('quiz/create/', QuizCreateView.as_view(), name='quiz-create'),
    path('quiz/bulk-create/', bulk_quiz_create_view, name='bulk-create'),
    path('quiz/<int:pk>/', QuizDetailView.as_view(), name='quiz-detail'),
    path('quiz/edit/<int:pk>/', quiz_edit_view, name='quiz-edit'),
    path('quiz/delete/<int:pk>/', quiz_delete_view, name='quiz-delete'),
    path('quiz/<int:pk>/question-create/', question_create_view, name='question-create'),
    path('question/<int:pk>/', QuestionDetailView.as_view(), name='question-detail'),
    path('question/edit/<int:pk>', question_edit_view, name='question-edit'),
    path('question/delete/<int:question_id>/', question_delete_view, name='question-delete'),
    path('question/<int:question_id>/answer-create/', answer_create_view, name='answer-create'),
    path('answer/delete/<int:pk>/', answer_delete_view, name='answer-delete'),
    #path('quiz/edit/<int:pk>/question/edit/<int:pk>/', question_edit_view, name='question-create'),
]
