from django.contrib import admin

from quiz.models import Quiz, Question, Answer, StudentTest, StudentTestAnswer

admin.site.register(Quiz)
admin.site.register(Question)
admin.site.register(Answer)
admin.site.register(StudentTest)
admin.site.register(StudentTestAnswer)



