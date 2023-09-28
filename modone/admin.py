from django.contrib import admin
from .models import *


admin.site.register(Semester)


class ChoiceAdmin(admin.StackedInline):
    model = Choice


class QuestionsAdmin(admin.ModelAdmin):
    inlines = [ChoiceAdmin]


admin.site.register(Question, QuestionsAdmin)
admin.site.register(Choice)
admin.site.register(ModOneUserQuiz)
admin.site.register(ModUserResponse)
