from django.contrib.auth.models import User
from django.db import models

SUBJECT = (
    ('mathematics', 'Математика'),
    ('history', 'История'),
    ('geography', 'Геогрфия'),
    ('physics', 'Физика'),
)


class Quiz(models.Model):
    title = models.CharField(max_length=255)
    subject = models.CharField(max_length=11, choices=SUBJECT)
    description = models.TextField()
    author = models.ForeignKey(User, on_delete=models.DO_NOTHING)

    class Meta:
        verbose_name_plural = "Quizzes"
        ordering = ['id']

    def __str__(self):
        return self.title


class Question(models.Model):
    author = models.ForeignKey(
        User,
        related_name='questions',
        on_delete=models.DO_NOTHING,
    )
    prompt = models.CharField(max_length=255)
    quiz = models.ManyToManyField(
        Quiz,
        related_name='questions',
    )
    subject = models.CharField(max_length=11, choices=SUBJECT)

    def __str__(self):
        return self.prompt


class Answer(models.Model):
    question = models.ForeignKey(
        Question,
        related_name='answers',
        on_delete=models.CASCADE
    )
    text = models.CharField(max_length=255)
    is_correct = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.text} => {"C" if self.is_correct else "NC"}'
