from django.contrib import admin
from .models import (
    Course,
    Instructor,
    Learner,
    Lesson,
    Question,
    Choice,
    Submission
)

class ChoiceInline(admin.TabularInline):
    model = Choice
    extra = 2


class QuestionInline(admin.TabularInline):
    model = Question
    extra = 1


class QuestionAdmin(admin.ModelAdmin):
    inlines = [ChoiceInline]


class LessonAdmin(admin.ModelAdmin):
    inlines = [QuestionInline]


admin.site.register(Course)
admin.site.register(Instructor)
admin.site.register(Learner)
admin.site.register(Lesson, LessonAdmin)
admin.site.register(Question, QuestionAdmin)
admin.site.register(Choice)
admin.site.register(Submission)
