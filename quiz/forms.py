from django import forms

from quiz.models import Quiz, Question, Answer, StudentTest
from registrator.models import TeacherProfile


class QuizCreateForm(forms.ModelForm):
    class Meta:
        model = Quiz
        exclude = ('subject', 'author')

    def save(self, user=None):
        quiz = super().save(commit=False)
        teacher_profile = TeacherProfile.objects.get(user=user)
        quiz.author = user
        quiz.subject = teacher_profile.subject
        quiz.save()
        return quiz


class BulkCreateForm(forms.Form):
    file = forms.FileField()


class QuestionCreateForm(forms.ModelForm):
    class Meta:
        model = Question
        exclude = ('author', 'subject', 'quiz')

    # def __init__(self, user, quiz_id=None, *args, **kwargs):
    #     super().__init__(*args, **kwargs)
    #     if not quiz_id:
    #         self.fields['quiz'] = forms.ModelChoiceField(queryset=Quiz.objects.filter(author=user))
    # else:
    #     self.fields['quiz'] = Quiz.objects.get(id=quiz_id)
    #     #self.fields['quiz']
    def save(self, user=None, quiz_id=None):
        question = super().save(commit=False)
        teacher_profile = TeacherProfile.objects.get(user=user)
        question.author = user
        question.subject = teacher_profile.subject
        question.quiz = Quiz.objects.get(id=quiz_id)
        question.save()
        return question


class AnswerCreateForm(forms.ModelForm):
    class Meta:
        model = Answer
        exclude = ('question',)

    # def __init__(self, user, *args, **kwargs):
    #     super().__init__(*args, **kwargs)
    #     self.fields['question'] = forms.ModelChoiceField(queryset=Question.objects.filter(author=user))
    def save(self, question_id):
        answer = super().save(commit=False)
        answer.question = Question.objects.get(id=question_id)
        answer.save()

class QuizAssignForm(forms.ModelForm):
    # quiz = forms.ModelMultipleChoiceField()
    class Meta:
        model = StudentTest
        exclude = ('is_compleated', 'score')

    def __init__(self, user, *args, **kwargs):
        super(QuizAssignForm, self).__init__(*args, **kwargs)
        self.fields['school_class'] = forms.ModelMultipleChoiceField(
            queryset=TeacherProfile.objects.get(user=user).school_class
        )
