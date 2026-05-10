from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    nickname = models.CharField(max_length=50, blank=True, verbose_name='暱稱')

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

    class Meta:
        verbose_name = '題目'
        verbose_name_plural = '題目'
        unique_together = ['chapter', 'question_number']
        ordering = ['chapter', 'question_number']

    def __str__(self):
        return f"{self.chapter} - 第{self.question_number}題"


class QuizRecord(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, verbose_name='使用者')
    chapter = models.CharField(max_length=50, verbose_name='章節')
    total_questions = models.IntegerField(verbose_name='總題數')
    correct_count = models.IntegerField(verbose_name='答對題數')
    score = models.FloatField(verbose_name='分數')
    time_spent = models.IntegerField(verbose_name='耗時(秒)', default=0)
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