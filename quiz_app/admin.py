from django.contrib import admin
from .models import Question, QuizRecord, WrongAnswer


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ['chapter', 'question_number', 'question_text', 'correct_answer', 'difficulty']
    list_filter = ['chapter', 'difficulty']
    search_fields = ['question_text']
    fieldsets = (
        ('基本資訊', {
            'fields': ('chapter', 'question_number', 'question_text', 'difficulty')
        }),
        ('選項', {
            'fields': ('option_a', 'option_b', 'option_c', 'option_d', 'option_e')
        }),
        ('答案', {
            'fields': ('correct_answer',)
        }),
    )


@admin.register(QuizRecord)
class QuizRecordAdmin(admin.ModelAdmin):
    list_display = ['chapter', 'total_questions', 'correct_count', 'score', 'time_spent', 'created_at']
    list_filter = ['chapter', 'created_at']
    search_fields = ['chapter']
    readonly_fields = ['created_at']


@admin.register(WrongAnswer)
class WrongAnswerAdmin(admin.ModelAdmin):
    list_display = ['question', 'user_answer', 'created_at']
    list_filter = ['question__chapter', 'created_at']
    search_fields = ['question__question_text']
    readonly_fields = ['created_at']