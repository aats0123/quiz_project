from django.shortcuts import render


def render_home(request):
    return render(request, 'quiz/home.html')

