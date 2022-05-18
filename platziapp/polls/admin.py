from django.contrib import admin
from .models import Choice, Question
class ChoiceInline(admin.TabularInline):
    model = Choice
class QuestionAdmin(admin.ModelAdmin):
    inlines = [
        ChoiceInline,
    ]

# admin.site.register(ChoiceInline)
admin.site.register(Question, QuestionAdmin)