import xml

from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView, FormView, DetailView, DeleteView
from django.views.generic.base import View
import xml.etree.ElementTree as xml_tree

from quiz.forms import QuizCreateForm, QuestionCreateForm, AnswerCreateForm
from quiz.models import Quiz, Question, Answer
from registrator.models import TeacherProfile, StudentProfile


def render_home(request):
    return render(request, 'quiz/home.html')


class StudentDetailView(DetailView):
    model = User
    template_name = 'quiz/student-detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        student_profile = StudentProfile.objects.get(user=self.request.user)
        context['profile'] = student_profile
        return context


class TeacherDetailView(DetailView):
    model = User
    template_name = 'quiz/teacher-detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        teacher_profile = TeacherProfile.objects.get(user=self.request.user)
        quizzes = Quiz.objects.filter(author=self.request.user)
        context['profile'] = teacher_profile
        context['quizzes'] = quizzes
        return context


class QuizDetailView(DetailView):
    model = Quiz
    template_name = 'quiz/quiz-detail.html'
    context_object_name = 'quiz'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        quiz = context['quiz']
        questions = Question.objects.filter(quiz=quiz)
        context['questions'] = questions
        return context


class QuizCreateView(FormView):
    form_class = QuizCreateForm
    template_name = 'quiz/quiz-create.html'
    success_url = reverse_lazy('quiz-home')
    teacher_id = None

    def form_valid(self, form):
        self.teacher_id = self.request.user.id
        form.save(self.request.user)
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('teacher-detail', kwargs={'pk': self.teacher_id})


@login_required
def bulk_quiz_create_view(request):
    if request.method == 'GET':
        return render(request, 'quiz/bulk-create.html')

    quiz_file = request.FILES['quiz-file']
    tree = xml_tree.parse(quiz_file)
    quiz_xml = tree.getroot()
    quiz_name = quiz_xml.attrib['title']
    quiz = Quiz(title=quiz_name, author=request.user, subject=request.user.teacherprofile.subject)
    quiz.save()
    for question_xml in quiz_xml:
        question = Question(
            prompt=question_xml.attrib['prompt'],
            subject=request.user.teacherprofile.subject,
            author=request.user,
            quiz=quiz
        )
        question.save()
        for answer_xml in question_xml:
            answer = Answer(
                text=answer_xml.text,
                is_correct=True if answer_xml.attrib['correct'].lower() == 'yes' else False,
                question=question
            )
            answer.save()
    return redirect('teacher-detail', request.user.id)





@login_required
def quiz_delete_view(request, pk):
    if request.method == 'GET':
        quiz = Quiz.objects.get(id=pk)
        return render(request, 'quiz/delete.html', {'quiz': quiz})
    quiz = Quiz.objects.get(id=pk)
    quiz.delete()
    return redirect('teacher-detail', quiz.author_id)


@login_required
def quiz_edit_view(request, pk):
    quiz = Quiz.objects.get(id=pk)
    if request.method == 'POST':
        form = QuizCreateForm(request.POST, instance=quiz)
        if form.is_valid():
            form.save(request.user)
            return redirect('teacher-detail', quiz.author_id)
    return render(request, 'quiz/quiz-create.html', {'form': QuizCreateForm(instance=quiz)})


@login_required
def question_create_view(request, pk):
    quiz = Quiz.objects.get(id=pk)
    if request.method == 'GET':
        form = QuestionCreateForm()
        context = {'form': form, 'quiz': quiz}
        return render(request, 'quiz/question-create.html', context)

    form = QuestionCreateForm(request.POST)
    if form.is_valid():
        form.save(request.user, pk)
        return redirect('quiz-detail', pk)
    return render(request, 'quiz/question-create.html', {'form': form, 'quiz': quiz})


class QuestionDetailView(DetailView):
    model = Question
    template_name = 'quiz/question-detail.html'
    context_object_name = 'question'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        question = context['question']
        context['answers'] = Answer.objects.filter(question=question)
        return context


@login_required
def question_edit_view(request, pk):
    pass


@login_required
def question_delete_view(request, question_id):
    question = Question.objects.get(id=question_id)
    quiz = question.quiz
    if request.method == 'GET':
        return render(request, 'quiz/delete.html', {'question': question})
    question.delete()
    return redirect('quiz-detail', quiz.id)


@login_required
def answer_create_view(request, question_id):
    if request.method == 'GET':
        return render(request, 'quiz/answer-create.html', {'form': AnswerCreateForm()})

    form = AnswerCreateForm(request.POST)
    if form.is_valid():
        form.save(question_id=question_id)
        return redirect('question-detail', question_id)

    return render('quiz/answer-create.html', question_id)


@login_required
def answer_delete_view(request, pk):
    answer = Answer.objects.get(id=pk)
    question = answer.question
    if request.method == 'GET':
        return render(request, 'quiz/delete.html', {'answer': answer})
    answer.delete()
    return redirect('question-detail', question.id)

@login_required
def quiz_assign_view(request):
    pass