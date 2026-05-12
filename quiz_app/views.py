from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from .models import Question, QuizRecord, WrongAnswer, User
import random


def quiz_home(request):
    return render(request, 'quiz_app/home.html', {'user': request.user})


def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect('home')
        else:
            return render(request, 'quiz_app/login.html', {'error': '帳號或密碼錯誤'})
    return render(request, 'quiz_app/login.html')


def register_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        nickname = request.POST.get('nickname')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        if password != confirm_password:
            return render(request, 'quiz_app/register.html', {'error': '密碼不一致'})

        if User.objects.filter(username=username).exists():
            return render(request, 'quiz_app/register.html', {'error': '帳號已存在'})

        user = User.objects.create_user(username=username, password=password, nickname=nickname)
        login(request, user)
        return redirect('home')

    return render(request, 'quiz_app/register.html')


def logout_view(request):
    logout(request)
    return redirect('home')


def random_quiz(request):
    if not request.user.is_authenticated:
        return redirect('login')

    all_questions = list(Question.objects.all())

    # 分離連貫題和非連貫題
    sequential_questions = [q for q in all_questions if q.sequence_group]
    non_sequential_questions = [q for q in all_questions if not q.sequence_group]

    # 對非連貫題進行隨機打亂
    random.shuffle(non_sequential_questions)

    # 對連貫題按組別和題號排序
    sequential_questions.sort(key=lambda q: (q.sequence_group, q.question_number))

    # 合併題目
    questions = non_sequential_questions + sequential_questions

    quiz_data = []
    for q in questions:
        options = [
            ('A', q.option_a),
            ('B', q.option_b),
            ('C', q.option_c),
        ]
        if q.option_d:
            options.append(('D', q.option_d))
        if q.option_e:
            options.append(('E', q.option_e))

        quiz_data.append({
            'id': q.id,
            'question': q.question_text,
            'question_image': q.question_image.url if q.question_image else None,
            'options': options,
            'correct_answer': q.correct_answer,
        })

    request.session['quiz_data'] = quiz_data
    request.session['chapter'] = '隨機測驗'
    request.session['start_time'] = None

    return render(request, 'quiz_app/quiz.html', {
        'quiz_data': quiz_data,
        'chapter': '隨機測驗',
    })


def start_quiz(request, chapter):
    if not request.user.is_authenticated:
        return redirect('login')

    questions = list(Question.objects.filter(chapter=chapter))
    random.shuffle(questions)

    quiz_data = []
    for q in questions:
        options = [
            ('A', q.option_a),
            ('B', q.option_b),
            ('C', q.option_c),
        ]
        if q.option_d:
            options.append(('D', q.option_d))
        if q.option_e:
            options.append(('E', q.option_e))

        quiz_data.append({
            'id': q.id,
            'question': q.question_text,
            'question_image': q.question_image.url if q.question_image else None,
            'options': options,
            'correct_answer': q.correct_answer,
        })

    request.session['quiz_data'] = quiz_data
    request.session['chapter'] = chapter
    request.session['start_time'] = None

    return render(request, 'quiz_app/quiz.html', {
        'quiz_data': quiz_data,
        'chapter': chapter,
    })


def submit_quiz(request):
    if request.method == 'POST':
        quiz_data = request.session.get('quiz_data', [])
        chapter = request.session.get('chapter', '')
        time_spent = int(request.POST.get('time_spent', 0))

        results = []
        correct_count = 0
        wrong_answers = []

        for item in quiz_data:
            question_id = item['id']
            correct_answer = item['correct_answer']
            user_answer = request.POST.get(f'question_{question_id}', '')

            is_correct = user_answer == correct_answer
            if is_correct:
                correct_count += 1
            else:
                wrong_answers.append({
                    'question_id': question_id,
                    'user_answer': user_answer,
                })

            results.append({
                'question': item['question'],
                'options': item['options'],
                'user_answer': user_answer,
                'correct_answer': correct_answer,
                'is_correct': is_correct,
            })

        total_questions = len(results)
        score = (correct_count / total_questions * 100) if total_questions > 0 else 0

        # 計算時間格式
        time_minutes = time_spent // 60
        time_seconds = time_spent % 60

        # 保存作答記錄
        quiz_record = QuizRecord.objects.create(
            user=request.user if request.user.is_authenticated else None,
            chapter=chapter,
            total_questions=total_questions,
            correct_count=correct_count,
            score=score,
            time_spent=time_spent,
        )

        # 保存錯題記錄
        for wrong in wrong_answers:
            question = Question.objects.get(id=wrong['question_id'])
            WrongAnswer.objects.create(
                quiz_record=quiz_record,
                question=question,
                user_answer=wrong['user_answer'],
            )

        return render(request, 'quiz_app/result.html', {
            'results': results,
            'correct_count': correct_count,
            'total_questions': total_questions,
            'score': score,
            'chapter': chapter,
            'time_spent': time_spent,
            'time_minutes': time_minutes,
            'time_seconds': time_seconds,
        })

    return render(request, 'quiz_app/home.html')


def quiz_records(request):
    if not request.user.is_authenticated:
        return redirect('login')
    records = QuizRecord.objects.filter(user=request.user).order_by('-created_at')[:20]
    return render(request, 'quiz_app/quiz_records.html', {'records': records})


def leaderboard(request):
    records = QuizRecord.objects.all().order_by('-score')[:20]
    # 為每個記錄計算時間格式
    for record in records:
        record.time_minutes = record.time_spent // 60
        record.time_seconds = record.time_spent % 60
    return render(request, 'quiz_app/leaderboard.html', {'records': records})


def wrong_answers(request):
    if not request.user.is_authenticated:
        return redirect('login')
    from django.db.models import Count
    records = QuizRecord.objects.filter(user=request.user).annotate(
        wrong_count=Count('wronganswer')
    ).filter(wrong_count__gt=0).order_by('-created_at')[:20]
    return render(request, 'quiz_app/wrong_answers.html', {'records': records})


def wrong_answers_detail(request, record_id):
    record = QuizRecord.objects.get(id=record_id)
    wrong_answers = WrongAnswer.objects.filter(quiz_record=record).select_related('question')

    wrong_data = []
    for wrong in wrong_answers:
        question = wrong.question
        options = [
            ('A', question.option_a),
            ('B', question.option_b),
            ('C', question.option_c),
        ]
        if question.option_d:
            options.append(('D', question.option_d))
        if question.option_e:
            options.append(('E', question.option_e))

        wrong_data.append({
            'wrong': wrong,
            'options': options,
        })

    return render(request, 'quiz_app/wrong_answers_detail.html', {
        'record': record,
        'wrong_answers': wrong_data,
    })


def review_wrong(request, wrong_id):
    wrong = WrongAnswer.objects.get(id=wrong_id)
    question = wrong.question

    options = [
        ('A', question.option_a),
        ('B', question.option_b),
        ('C', question.option_c),
    ]
    if question.option_d:
        options.append(('D', question.option_d))
    if question.option_e:
        options.append(('E', question.option_e))

    return render(request, 'quiz_app/review_wrong.html', {
        'question': question,
        'options': options,
        'user_answer': wrong.user_answer,
        'correct_answer': question.correct_answer,
    })