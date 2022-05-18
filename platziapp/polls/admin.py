from django.contrib import admin
from .models import Choice, Question
class ChoiceInline(admin.TabularInline):
    model = Choice
    extra = 3
class QuestionAdmin(admin.ModelAdmin):
    fields = ["pub_date", "question_text"]
    inlines = [
        ChoiceInline,
    ]

# admin.site.register(ChoiceInline)
admin.site.register(Question, QuestionAdmin)