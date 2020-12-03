from django.contrib import admin

# Register your models here.
from registrator.models import School, TeacherProfile, StudentProfile, StudentTest

admin.site.register(School)
admin.site.register(TeacherProfile)
admin.site.register(StudentProfile)
admin.site.register(StudentTest)
