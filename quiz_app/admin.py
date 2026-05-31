from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.html import format_html
from .models import Question, QuizRecord, WrongAnswer, User


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = ['username', 'nickname', 'email', 'is_staff']
    list_filter = ['is_staff', 'is_superuser']
    search_fields = ['username', 'nickname', 'email']

    # 添加 nickname 欄位到 fieldsets
    fieldsets = BaseUserAdmin.fieldsets + (
        ('額外資訊', {'fields': ('nickname',)}),
    )

    # 添加 nickname 欄位到 add_fieldsets
    add_fieldsets = BaseUserAdmin.add_fieldsets + (
        ('額外資訊', {'fields': ('nickname',)}),
    )


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ['chapter', 'question_number', 'question_text_preview', 'correct_answer', 'difficulty', 'is_new', 'show_image']
    list_filter = ['chapter', 'difficulty', 'is_new']
    search_fields = ['question_text']
    fieldsets = (
        ('基本資訊', {
            'fields': ('chapter', 'question_number', 'question_text', 'difficulty')
        }),
        ('題目圖片', {
            'fields': ('question_image',),
            'description': '只有第11題和第16題需要圖片'
        }),
        ('選項', {
            'fields': ('option_a', 'option_b', 'option_c', 'option_d', 'option_e')
        }),
        ('答案', {
            'fields': ('correct_answer',)
        }),
        ('題目來源', {
            'fields': ('is_new', 'source_note'),
            'classes': ('wide',),
            'description': '自編題目請勾選「自編題目」並填寫來源說明'
        }),
        ('題目詳解', {
            'fields': ('explanation',),
            'classes': ('wide',),
            'description': '作答後顯示的詳細解析（若留空則不顯示）'
        }),
    )

    def question_text_preview(self, obj):
        return obj.question_text[:50] + '...' if len(obj.question_text) > 50 else obj.question_text
    question_text_preview.short_description = '題目'

    def show_image(self, obj):
        if obj.question_image:
            return format_html('<img src="{}" width="50" height="50" />', obj.question_image.url)
        return '無圖片'
    show_image.short_description = '圖片'


@admin.register(QuizRecord)
class QuizRecordAdmin(admin.ModelAdmin):
    list_display = ['user', 'chapter', 'total_questions', 'correct_count', 'score', 'time_spent', 'is_sr', 'created_at']
    list_filter = ['chapter', 'created_at']
    search_fields = ['chapter', 'user__username']
    readonly_fields = ['created_at']


@admin.register(WrongAnswer)
class WrongAnswerAdmin(admin.ModelAdmin):
    list_display = ['question', 'user_answer', 'created_at']
    list_filter = ['question__chapter', 'created_at']
    search_fields = ['question__question_text']
    readonly_fields = ['created_at']