import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'quiz_project.settings')
django.setup()

from quiz_app.models import Question
from django.core.files import File

# 更新第11題和第16題的圖片
q11 = Question.objects.filter(question_number=11).first()
q16 = Question.objects.filter(question_number=16).first()

# 檢查圖片文件是否存在
image_11_path = 'quiz_app/static/quiz_app/images/question_11.png'
image_16_path = 'quiz_app/static/quiz_app/images/question_16.png'

if q11:
    if q11.question_image:
        q11.question_image.delete(save=False)
    if os.path.exists(image_11_path):
        with open(image_11_path, 'rb') as f:
            file_obj = File(f, name='question_11.png')
            q11.question_image.save('question_11.png', file_obj, save=False)
    q11.save()
    print('Question 11 image updated')

if q16:
    if q16.question_image:
        q16.question_image.delete(save=False)
    if os.path.exists(image_16_path):
        with open(image_16_path, 'rb') as f:
            file_obj = File(f, name='question_16.png')
            q16.question_image.save('question_16.png', file_obj, save=False)
    q16.save()
    print('Question 16 image updated')

# Clear other questions' images
print('\nClearing other questions images...')
for q in Question.objects.all():
    if q.question_number not in [11, 16] and q.question_image:
        q.question_image.delete(save=False)
        q.question_image = ''
        q.save()
        print(f'Question {q.question_number} image cleared')

print('Done!')
