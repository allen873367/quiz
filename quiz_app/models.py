from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    nickname = models.CharField(max_length=50, blank=True, verbose_name='暱稱')
    student_class = models.CharField(max_length=50, blank=True, null=True, verbose_name='班級')
    is_teacher = models.BooleanField(default=False, verbose_name='教師身分')

    class Meta:
        verbose_name = '使用者'
        verbose_name_plural = '使用者'

    def __str__(self):
        return self.nickname or self.username


class Question(models.Model):
    DIFFICULTY_CHOICES = [
        ('easy', '簡單'),
        ('medium', '中等'),
        ('hard', '困難'),
    ]

    chapter = models.CharField(max_length=50, verbose_name='章節')
    question_number = models.IntegerField(verbose_name='題號')
    question_text = models.TextField(verbose_name='題目')
    question_image = models.ImageField(
        upload_to='quiz_app/images/',
        blank=True,
        null=True,
        verbose_name='題目圖片'
    )
    option_a = models.CharField(max_length=500, verbose_name='選項A')
    option_b = models.CharField(max_length=500, verbose_name='選項B')
    option_c = models.CharField(max_length=500, verbose_name='選項C')
    option_d = models.CharField(max_length=500, blank=True, null=True, verbose_name='選項D')
    option_e = models.CharField(max_length=500, blank=True, null=True, verbose_name='選項E')
    correct_answer = models.CharField(max_length=1, verbose_name='正確答案')
    difficulty = models.CharField(
        max_length=10,
        choices=DIFFICULTY_CHOICES,
        default='medium',
        verbose_name='難易度'
    )
    sequence_group = models.CharField(
        max_length=50,
        blank=True,
        null=True,
        verbose_name='連貫題組別',
        help_text='同一組別的題目會保持順序'
    )
    is_new = models.BooleanField(default=False, verbose_name='自編題目')
    source_note = models.CharField(
        max_length=200, blank=True, verbose_name='題目來源',
        help_text='若為自編題目，請註明來源或設計說明'
    )
    explanation = models.TextField(
        blank=True, verbose_name='題目詳解',
        help_text='作答後顯示的詳細解析，說明為什麼正確答案是對的'
    )
    error_count = models.IntegerField(default=0, verbose_name='累計錯誤次數')
    total_attempt_count = models.IntegerField(default=0, verbose_name='累計答題次數')

    class Meta:
        verbose_name = '題目'
        verbose_name_plural = '題目'
        unique_together = ['chapter', 'question_number']
        ordering = ['chapter', 'question_number']

    def __str__(self):
        return f"{self.chapter} - 第{self.question_number}題"

    @property
    def error_rate(self):
        """回傳錯誤率（0~100），若無答題記錄則回傳 0"""
        if self.total_attempt_count > 0:
            return round(self.error_count / self.total_attempt_count * 100, 1)
        return 0.0

    @property
    def is_boss_question(self):
        """錯誤率 >= 70% 且至少有 5 次答題記錄 → 魔王題"""
        return self.total_attempt_count >= 5 and self.error_rate >= 70


class QuizRecord(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, verbose_name='使用者')
    chapter = models.CharField(max_length=50, verbose_name='章節')
    total_questions = models.IntegerField(verbose_name='總題數')
    correct_count = models.IntegerField(verbose_name='答對題數')
    score = models.FloatField(verbose_name='分數')
    time_spent = models.IntegerField(verbose_name='耗時(秒)', default=0)
    is_sr = models.BooleanField(default=False, verbose_name='間隔學習法')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='作答時間')

    class Meta:
        verbose_name = '作答記錄'
        verbose_name_plural = '作答記錄'
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.chapter} - {self.score}分 ({self.created_at.strftime('%Y-%m-%d %H:%M')})"


class WrongAnswer(models.Model):
    quiz_record = models.ForeignKey(QuizRecord, on_delete=models.CASCADE, verbose_name='作答記錄')
    question = models.ForeignKey(Question, on_delete=models.CASCADE, verbose_name='題目')
    user_answer = models.CharField(max_length=1, verbose_name='使用者答案')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='作答時間')

    class Meta:
        verbose_name = '錯題記錄'
        verbose_name_plural = '錯題記錄'
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.question.chapter} - 第{self.question.question_number}題"


class Classroom(models.Model):
    name = models.CharField(max_length=100, verbose_name='班級名稱')
    teacher = models.ForeignKey(User, on_delete=models.CASCADE, related_name='classrooms', verbose_name='教師')
    invite_code = models.CharField(max_length=20, unique=True, verbose_name='邀請碼')
    description = models.TextField(blank=True, verbose_name='班級描述')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='建立時間')
    is_active = models.BooleanField(default=True, verbose_name='啟用中')

    class Meta:
        verbose_name = '班級'
        verbose_name_plural = '班級'
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.name} ({self.teacher.nickname})"


class ClassroomEnrollment(models.Model):
    classroom = models.ForeignKey(Classroom, on_delete=models.CASCADE, related_name='enrollments', verbose_name='班級')
    student = models.ForeignKey(User, on_delete=models.CASCADE, related_name='enrollments', verbose_name='學生')
    joined_at = models.DateTimeField(auto_now_add=True, verbose_name='加入時間')

    class Meta:
        verbose_name = '班級成員'
        verbose_name_plural = '班級成員'
        unique_together = ['classroom', 'student']
        ordering = ['joined_at']

    def __str__(self):
        return f"{self.student.nickname} → {self.classroom.name}"