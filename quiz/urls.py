from django.urls import path

from quiz.views import render_home

urlpatterns = [
    path('', render_home, name='quiz-home'),
]