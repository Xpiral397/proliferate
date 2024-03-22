from django.contrib import admin
from .models import *
# Register your models here.
admin.site.register(Profile)
admin.site.register(TutorProfile)
admin.site.register(TutorVerifictions)
admin.site.register(StudentProfile)
admin.site.register(Class)
admin.site.register(Subject)
admin.site.register(classSchedule)
admin.site.register(Assignment)