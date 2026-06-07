from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.db import models
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone
from datetime import timedelta
from .models import Question, QuizRecord, WrongAnswer, User, Classroom, ClassroomEnrollment
import random
import json
from collections import OrderedDict


def quiz_home(request):
    # 用 Python set 去重，避免 SQLite distinct 在 Unicode 上的問題
    raw_chapters = list(Question.objects.values_list('chapter', flat=True))
    unique_chapters = sorted(set(raw_chapters))
    chapter_count = len(unique_chapters)
    total_questions = Question.objects.count()
    new_questions = Question.objects.filter(is_new=True).count()

    chapters_data = []
    for ch in unique_chapters:
        count = Question.objects.filter(chapter=ch).count()
        chapters_data.append({
            'chapter': ch,
            'count': count,
        })

    return render(request, 'quiz_app/home.html', {
        'user': request.user,
        'chapters': chapters_data,
        'total_questions': total_questions,
        'new_questions': new_questions,
        'chapter_count': chapter_count,
    })


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


def _build_shuffled_options(q):
    """建立標籤固定為 A、B、C、D、E，但內容隨機排列的選項，並回傳對應的正確答案字母"""
    label_order = ['A', 'B', 'C', 'D', 'E']

    # 收集選項內容（按 A→B→C→D→E 順序）
    option_texts = [q.option_a, q.option_b, q.option_c]
    if q.option_d:
        option_texts.append(q.option_d)
    if q.option_e:
        option_texts.append(q.option_e)
    # 只取有實際內容的標籤
    labels = label_order[:len(option_texts)]

    # 記錄正確答案對應的內容
    correct_idx = label_order.index(q.correct_answer)
    correct_text = option_texts[correct_idx] if correct_idx < len(option_texts) else ''

    # 隨機打亂內容
    random.shuffle(option_texts)

    # 固定標籤配上打亂後的內容
    options = list(zip(labels, option_texts))

    # 找出正確內容現在落在哪個標籤
    computed_answer = q.correct_answer  # fallback
    for label, text in options:
        if text == correct_text:
            computed_answer = label
            break

    return options, computed_answer


def _sample_with_groups(questions, count):
    """取 questions 中的 count 題

    所有情況：連貫題組（sequence_group）整組保留不拆散且組內按題號排序
    - count >= 總數：回傳全部，但連貫題組內保持順序
    - count < 總數：隨機抽，連貫題整組保留
    """
    # 分組：有 sequence_group 的整組一起，沒有的各自一題
    seq_map = OrderedDict()
    singles = []
    for q in questions:
        if q.sequence_group:
            seq_map.setdefault(q.sequence_group, []).append(q)
        else:
            singles.append(q)

    # 連貫題組內按題號排序（保持 11→12→13 順序）
    for g in seq_map.values():
        g.sort(key=lambda x: x.question_number)

    # 建立群組列表（一個群組可能含多題）並打亂
    groups = list(seq_map.values()) + [[q] for q in singles]
    random.shuffle(groups)

    # 整組加入，直到達到 count 為止
    result = []
    for g in groups:
        result.extend(g)
        if count is not None and len(result) >= count:
            break

    return result


def random_quiz(request):
    """跳轉到隨機挑戰設定頁面"""
    if not request.user.is_authenticated:
        return redirect('login')
    return redirect('random_quiz_setup')


def start_quiz(request, chapter):
    if not request.user.is_authenticated:
        return redirect('login')

    total = Question.objects.filter(chapter=chapter).count()
    estimated_minutes = max(5, total)

    # 取得最近一次記錄
    recent_record = QuizRecord.objects.filter(
        user=request.user, chapter=chapter
    ).order_by('-created_at').first()

    # 產生章節縮寫
    chapter_slug = chapter.replace(' ', '_').replace('　', '_')

    return render(request, 'quiz_app/quiz.html', {
        'chapter': chapter,
        'chapter_slug': chapter_slug,
        'total': total,
        'estimated_minutes': estimated_minutes,
        'recent_record': recent_record,
        'user': request.user,
    })


def random_quiz_setup(request):
    """隨機挑戰設定頁面 — 可選題數、章節、間隔學習"""
    if not request.user.is_authenticated:
        return redirect('login')

    chapters = Question.objects.values_list('chapter', flat=True).distinct().order_by('chapter')
    total_all = Question.objects.count()

    return render(request, 'quiz_app/random_quiz_setup.html', {
        'chapters': chapters,
        'total': total_all,
    })


def take_random_quiz(request):
    """接收設定參數，建立混題測驗"""
    if not request.user.is_authenticated:
        return redirect('login')

    selected_chapters = request.GET.getlist('chapters')
    count = request.GET.get('count', None)
    sr = request.GET.get('sr', '0') == '1'

    if selected_chapters:
        questions = list(Question.objects.filter(chapter__in=selected_chapters))
    else:
        # 沒選章節 = 全部
        questions = list(Question.objects.all())

    if not questions:
        return redirect('random_quiz_setup')

    random.shuffle(questions)

    # 根據 count 限制題數（保留連貫題組）
    if count is not None:
        try:
            count = int(count)
            questions = _sample_with_groups(questions, count)
        except (ValueError, TypeError):
            pass

    quiz_data = []
    for q in questions:
        options, computed_answer = _build_shuffled_options(q)
        quiz_data.append({
            'id': q.id,
            'question': q.question_text,
            'question_image': q.question_image.url if q.question_image else None,
            'options': options,
            'correct_answer': computed_answer,
            'difficulty': q.get_difficulty_display() if hasattr(q, 'get_difficulty_display') else '',
            'explanation': q.explanation or '',
        })

    request.session['quiz_data'] = quiz_data
    request.session['chapter'] = '隨機測驗'
    request.session['start_time'] = None
    request.session['sr_enabled'] = sr
    request.session['sr_wrong_ids'] = []
    request.session['sr_round'] = 0
    if sr:
        request.session['sr_original_total'] = len(questions)
        request.session['sr_first_correct'] = 0
        request.session['sr_cumulative_time'] = 0

    return render(request, 'quiz_app/take_quiz.html', {
        'quiz_data': quiz_data,
        'chapter': '隨機測驗',
    })


def take_quiz(request, chapter):
    if not request.user.is_authenticated:
        return redirect('login')

    count = request.GET.get('count', None)
    sr = request.GET.get('sr', '0') == '1'

    questions = list(Question.objects.filter(chapter=chapter))
    random.shuffle(questions)

    # 根據 count 限制題數（保留連貫題組）
    if count is not None:
        try:
            count = int(count)
            questions = _sample_with_groups(questions, count)
        except (ValueError, TypeError):
            pass

    quiz_data = []
    for q in questions:
        options, computed_answer = _build_shuffled_options(q)
        quiz_data.append({
            'id': q.id,
            'question': q.question_text,
            'question_image': q.question_image.url if q.question_image else None,
            'options': options,
            'correct_answer': computed_answer,
            'difficulty': q.get_difficulty_display() if hasattr(q, 'get_difficulty_display') else '',
            'explanation': q.explanation or '',
        })

    request.session['quiz_data'] = quiz_data
    request.session['chapter'] = chapter
    request.session['start_time'] = None
    request.session['sr_enabled'] = sr
    request.session['sr_wrong_ids'] = []  # 用於間隔學習的錯題 ID
    request.session['sr_round'] = 0
    if sr:
        request.session['sr_original_total'] = len(questions)
        request.session['sr_first_correct'] = 0   # 第一輪答對數（評分依據）
        request.session['sr_cumulative_time'] = 0  # 所有輪次總時間

    return render(request, 'quiz_app/take_quiz.html', {
        'quiz_data': quiz_data,
        'chapter': chapter,
    })


def submit_quiz(request):
    if request.method == 'POST':
        quiz_data = request.session.get('quiz_data', [])
        chapter = request.session.get('chapter', '')
        sr_enabled = request.session.get('sr_enabled', False)
        sr_wrong_ids = request.session.get('sr_wrong_ids', [])
        sr_round = request.session.get('sr_round', 0)
        sr_original_total = request.session.get('sr_original_total')
        sr_first_correct = request.session.get('sr_first_correct', 0)
        sr_cumulative_time = request.session.get('sr_cumulative_time', 0)
        time_spent = int(request.POST.get('time_spent', 0))

        results = []
        correct_count = 0
        wrong_answers = []
        new_wrong_ids = []

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
                if question_id not in new_wrong_ids:
                    new_wrong_ids.append(question_id)

            results.append({
                'question': item['question'],
                'options': item['options'],
                'user_answer': user_answer,
                'correct_answer': correct_answer,
                'is_correct': is_correct,
                'explanation': item.get('explanation', ''),
            })

        total_questions = len(results)

        # ─── 間隔學習邏輯 ───
        if sr_enabled:
            if sr_round == 0:
                # 第一輪：記錄原始答對數（作為最終評分依據）
                request.session['sr_first_correct'] = correct_count
                request.session['sr_cumulative_time'] = time_spent

                if new_wrong_ids:
                    # 有錯題 → 保存第一輪完整結果，只出錯題進入間隔學習
                    request.session['sr_full_results'] = results

                    # 更新第一輪的題目錯誤率統計
                    for item in quiz_data:
                        qid = item['id']
                        try:
                            q = Question.objects.get(id=qid)
                            q.total_attempt_count = models.F('total_attempt_count') + 1
                            q.save(update_fields=['total_attempt_count'])
                        except Question.DoesNotExist:
                            pass
                    for wrong in wrong_answers:
                        try:
                            q = Question.objects.get(id=wrong['question_id'])
                            q.error_count = models.F('error_count') + 1
                            q.save(update_fields=['error_count'])
                        except Question.DoesNotExist:
                            pass

                    sr_wrong_ids = new_wrong_ids[:]
                    wrong_qs = list(Question.objects.filter(id__in=sr_wrong_ids))
                    random.shuffle(wrong_qs)
                    sr_quiz_data = []
                    for q in wrong_qs:
                        options, computed_answer = _build_shuffled_options(q)
                        sr_quiz_data.append({
                            'id': q.id,
                            'question': q.question_text,
                            'question_image': q.question_image.url if q.question_image else None,
                            'options': options,
                            'correct_answer': computed_answer,
                            'difficulty': q.get_difficulty_display() if hasattr(q, 'get_difficulty_display') else '',
                            'explanation': q.explanation or '',
                        })
                    request.session['quiz_data'] = sr_quiz_data
                    request.session['sr_wrong_ids'] = sr_wrong_ids
                    request.session['sr_round'] = 1
                    return render(request, 'quiz_app/take_quiz.html', {
                        'quiz_data': sr_quiz_data,
                        'chapter': chapter,
                        'sr_round': 1,
                    })
                # 第一輪全對 → 直接結算（不進 SR）
            else:
                # ── 間隔學習輪次（sr_round >= 1）──
                # 累計時間
                request.session['sr_cumulative_time'] = sr_cumulative_time + time_spent

                # 移除此次答對的題目：只保留仍然答錯的 ID
                sr_wrong_ids = new_wrong_ids[:]
                request.session['sr_wrong_ids'] = sr_wrong_ids

                if sr_wrong_ids:
                    # 還有錯題 → 繼續下一輪（無上限次數）
                    wrong_qs = list(Question.objects.filter(id__in=sr_wrong_ids))
                    random.shuffle(wrong_qs)
                    sr_quiz_data = []
                    for q in wrong_qs:
                        options, computed_answer = _build_shuffled_options(q)
                        sr_quiz_data.append({
                            'id': q.id,
                            'question': q.question_text,
                            'question_image': q.question_image.url if q.question_image else None,
                            'options': options,
                            'correct_answer': computed_answer,
                            'difficulty': q.get_difficulty_display() if hasattr(q, 'get_difficulty_display') else '',
                            'explanation': q.explanation or '',
                        })
                    request.session['quiz_data'] = sr_quiz_data
                    request.session['sr_round'] = sr_round + 1
                    return render(request, 'quiz_app/take_quiz.html', {
                        'quiz_data': sr_quiz_data,
                        'chapter': chapter,
                        'sr_round': sr_round + 1,
                    })
                # 全部答對 → 結算

        # ─── 結算（非 SR 或 SR 完成）───
        if sr_enabled and sr_original_total:
            # SR：使用第一輪答對數作為評分基準
            final_total = sr_original_total
            final_correct = sr_first_correct
            final_time = request.session['sr_cumulative_time']
            # 使用第一輪完整結果顯示答題詳解
            sr_full_results = request.session.get('sr_full_results', results)
            display_results = sr_full_results
        else:
            final_total = total_questions
            final_correct = correct_count
            final_time = time_spent
            display_results = results
        final_score = (final_correct / final_total * 100) if final_total > 0 else 0

        # 保存作答記錄
        quiz_record = QuizRecord.objects.create(
            user=request.user if request.user.is_authenticated else None,
            chapter=chapter,
            total_questions=final_total,
            correct_count=final_correct,
            score=final_score,
            time_spent=final_time,
            is_sr=sr_enabled,
        )

        # 保存錯題記錄（SR 使用第一輪的錯題資料）
        if sr_enabled and sr_original_total and sr_full_results:
            # 建立 question_text → Question 的查詢表，避免重複查詢
            wrong_qs = [item for item in sr_full_results if not item['is_correct']]
            q_ids = []
            for item in quiz_data:
                q_ids.append(item['id'])
            wrong_questions = Question.objects.filter(id__in=q_ids)
            q_map = {q.id: q for q in wrong_questions}
            for item in wrong_qs:
                # 從 display_results 的 question text 找對應的 question id
                qid = None
                for qi in quiz_data:
                    if qi['question'] == item['question']:
                        qid = qi['id']
                        break
                if qid and qid in q_map:
                    WrongAnswer.objects.create(
                        quiz_record=quiz_record,
                        question=q_map[qid],
                        user_answer=item['user_answer'],
                    )
        else:
            for wrong in wrong_answers:
                question = Question.objects.get(id=wrong['question_id'])
                WrongAnswer.objects.create(
                    quiz_record=quiz_record,
                    question=question,
                    user_answer=wrong['user_answer'],
                )

        # 更新題目的錯誤率統計（SR 已在 round 0 時計數，避免重複累計）
        if not sr_enabled:
            for item in quiz_data:
                qid = item['id']
                try:
                    q = Question.objects.get(id=qid)
                    q.total_attempt_count = models.F('total_attempt_count') + 1
                    q.save(update_fields=['total_attempt_count'])
                except Question.DoesNotExist:
                    pass
            for wrong in wrong_answers:
                try:
                    q = Question.objects.get(id=wrong['question_id'])
                    q.error_count = models.F('error_count') + 1
                    q.save(update_fields=['error_count'])
                except Question.DoesNotExist:
                    pass

        # 清除 SR session
        request.session.pop('sr_enabled', None)
        request.session.pop('sr_wrong_ids', None)
        request.session.pop('sr_round', None)
        request.session.pop('sr_original_total', None)
        request.session.pop('sr_first_correct', None)
        request.session.pop('sr_cumulative_time', None)
        request.session.pop('sr_full_results', None)

        # 時間格式
        time_minutes = final_time // 60
        time_seconds = final_time % 60

        return render(request, 'quiz_app/result.html', {
            'results': display_results,
            'correct_count': final_correct,
            'total_questions': final_total,
            'score': final_score,
            'chapter': chapter,
            'time_spent': final_time,
            'time_minutes': time_minutes,
            'time_seconds': time_seconds,
            'sr_used': sr_enabled,
            'sr_rounds': sr_round + 1 if sr_enabled else 0,
        })

    return render(request, 'quiz_app/home.html')


def quiz_records(request):
    if not request.user.is_authenticated:
        return redirect('login')
    mode = request.GET.get('mode', 'general')
    chapter = request.GET.get('chapter', '')
    q_count = request.GET.get('count', '')
    qs = QuizRecord.objects.filter(user=request.user)
    if mode == 'sr':
        qs = qs.filter(is_sr=True)
    else:
        qs = qs.filter(is_sr=False)
    if chapter:
        qs = qs.filter(chapter=chapter)
    if q_count:
        try:
            qs = qs.filter(total_questions=int(q_count))
        except ValueError:
            pass
    records = qs.order_by('-created_at')[:20]
    chapters_list = sorted(set(
        QuizRecord.objects.values_list('chapter', flat=True)
    ))
    return render(request, 'quiz_app/quiz_records.html', {
        'records': records,
        'mode': mode,
        'chapters': chapters_list,
        'selected_chapter': chapter,
        'selected_count': q_count,
    })


def leaderboard(request):
    """一般排行榜（支援章節與題數篩選）"""
    chapter = request.GET.get('chapter', '')
    q_count = request.GET.get('count', '')
    qs = QuizRecord.objects.filter(is_sr=False)
    if chapter:
        qs = qs.filter(chapter=chapter)
    if q_count:
        try:
            qs = qs.filter(total_questions=int(q_count))
        except ValueError:
            pass
    records = qs.order_by('-score')[:20]
    for record in records:
        record.time_minutes = record.time_spent // 60
        record.time_seconds = record.time_spent % 60

    # 取得所有出現過的章節
    chapters_list = sorted(set(
        QuizRecord.objects.values_list('chapter', flat=True)
    ))
    return render(request, 'quiz_app/leaderboard.html', {
        'records': records,
        'mode': 'general',
        'chapters': chapters_list,
        'selected_chapter': chapter,
        'selected_count': q_count,
    })


def sr_leaderboard(request):
    # 間隔學習排行榜：按時間升序（最快完成排第一）
    chapter = request.GET.get('chapter', '')
    q_count = request.GET.get('count', '')
    qs = QuizRecord.objects.filter(is_sr=True)
    if chapter:
        qs = qs.filter(chapter=chapter)
    if q_count:
        try:
            qs = qs.filter(total_questions=int(q_count))
        except ValueError:
            pass
    records = qs.order_by('time_spent')[:20]
    for record in records:
        record.time_minutes = record.time_spent // 60
        record.time_seconds = record.time_spent % 60

    chapters_list = sorted(set(
        QuizRecord.objects.values_list('chapter', flat=True)
    ))
    return render(request, 'quiz_app/leaderboard.html', {
        'records': records,
        'mode': 'sr',
        'chapters': chapters_list,
        'selected_chapter': chapter,
        'selected_count': q_count,
    })


def wrong_answers(request):
    if not request.user.is_authenticated:
        return redirect('login')
    from django.db.models import Count
    chapter = request.GET.get('chapter', '')
    qs = QuizRecord.objects.filter(user=request.user)
    if chapter:
        qs = qs.filter(chapter=chapter)
    records = qs.annotate(
        wrong_count=Count('wronganswer')
    ).filter(wrong_count__gt=0).order_by('-created_at')[:20]
    chapters_list = sorted(set(
        QuizRecord.objects.values_list('chapter', flat=True)
    ))
    return render(request, 'quiz_app/wrong_answers.html', {
        'records': records,
        'chapters': chapters_list,
        'selected_chapter': chapter,
    })


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
            'explanation': question.explanation or '',
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


def admin_panel(request):
    """自訂管理後台"""
    if not request.user.is_authenticated or not request.user.is_staff:
        messages.error(request, '你不是管理員')
        return redirect('home')

    raw_chapters = list(Question.objects.values_list('chapter', flat=True))
    unique_chapters = sorted(set(raw_chapters))
    total_questions = Question.objects.count()
    new_questions = Question.objects.filter(is_new=True).count()
    total_users = User.objects.count()
    total_records = QuizRecord.objects.count()

    chapters_data = []
    for ch in unique_chapters:
        count = Question.objects.filter(chapter=ch).count()
        chapters_data.append({
            'chapter': ch,
            'count': count,
        })

    # 搜集所有題目（含來源標記）
    questions = []
    for q in Question.objects.all().order_by('question_number'):
        questions.append({
            'id': q.id,
            'chapter': q.chapter,
            'number': q.question_number,
            'text': q.question_text[:80] + '...' if len(q.question_text) > 80 else q.question_text,
            'option_a': q.option_a[:30] + '...' if q.option_a and len(q.option_a) > 30 else (q.option_a or ''),
            'option_b': q.option_b[:30] + '...' if q.option_b and len(q.option_b) > 30 else (q.option_b or ''),
            'option_c': q.option_c[:30] + '...' if q.option_c and len(q.option_c) > 30 else (q.option_c or ''),
            'option_d': q.option_d[:30] + '...' if q.option_d and len(q.option_d) > 30 else (q.option_d or ''),
            'option_e': q.option_e[:30] + '...' if q.option_e and len(q.option_e) > 30 else (q.option_e or ''),
            'correct_answer': q.correct_answer,
            'difficulty': q.get_difficulty_display(),
            'is_new': q.is_new,
            'has_image': bool(q.question_image),
        })

    # 測驗統計
    records = QuizRecord.objects.all().order_by('-created_at')[:20]
    records_data = []
    for r in records:
        records_data.append({
            'id': r.id,
            'user': str(r.user.nickname or r.user.username),
            'chapter': r.chapter,
            'score': r.score,
            'correct_count': r.correct_count,
            'total': r.total_questions,
            'time_spent': r.time_spent,
            'is_sr': r.is_sr,
            'date': r.created_at.strftime('%m/%d %H:%M'),
        })

    # 班級列表（供建立/刪除班級 Modal 使用）
    class_list = (
        User.objects
        .filter(student_class__isnull=False)
        .exclude(student_class='')
        .values('student_class')
        .annotate(count=models.Count('id'))
        .order_by('student_class')
    )

    # 資訊面板下拉選單用
    info_users = User.objects.all().order_by('username').values('id', 'username', 'nickname')
    info_questions = Question.objects.all().order_by('chapter', 'question_number').values('id', 'chapter', 'question_number', 'question_text')

    return render(request, 'quiz_app/admin_panel.html', {
        'chapters': chapters_data,
        'questions': questions,
        'records': records_data,
        'users': User.objects.all().order_by('username'),
        'total_questions': total_questions,
        'new_questions': new_questions,
        'total_users': total_users,
        'total_records': total_records,
        'class_list': class_list,
        'info_users': info_users,
        'info_questions': info_questions,
    })


@require_http_methods(['GET'])
def api_get_question(request, qid):
    """回傳單一題目的 JSON 資料（供 admin modal 編輯用）"""
    if not request.user.is_authenticated or not request.user.is_staff:
        return JsonResponse({'error': '未授權'}, status=403)

    try:
        q = Question.objects.get(id=qid)
    except Question.DoesNotExist:
        return JsonResponse({'error': '題目不存在'}, status=404)

    return JsonResponse({
        'id': q.id,
        'chapter': q.chapter,
        'question_number': q.question_number,
        'question_text': q.question_text,
        'question_image': q.question_image.url if q.question_image else None,
        'option_a': q.option_a,
        'option_b': q.option_b,
        'option_c': q.option_c,
        'option_d': q.option_d or '',
        'option_e': q.option_e or '',
        'correct_answer': q.correct_answer,
        'difficulty': q.difficulty,
        'is_new': q.is_new,
        'explanation': q.explanation or '',
    })


@csrf_exempt
@require_http_methods(['POST'])
def api_update_question(request, qid):
    """接收表單資料更新題目（供 admin modal 儲存用）"""
    if not request.user.is_authenticated or not request.user.is_staff:
        return JsonResponse({'error': '未授權'}, status=403)

    try:
        q = Question.objects.get(id=qid)
    except Question.DoesNotExist:
        return JsonResponse({'error': '題目不存在'}, status=404)

    # 支援 JSON 和 multipart/form-data
    try:
        if request.content_type and 'application/json' in request.content_type:
            data = json.loads(request.body)
        else:
            data = request.POST.dict()
    except (json.JSONDecodeError, AttributeError):
        data = request.POST.dict()

    # 可更新的欄位
    try:
        q.chapter = data.get('chapter', q.chapter)
        q.question_number = int(data.get('question_number', q.question_number))
        q.question_text = data.get('question_text', q.question_text)
        q.option_a = data.get('option_a', q.option_a)
        q.option_b = data.get('option_b', q.option_b)
        q.option_c = data.get('option_c', q.option_c)
        q.option_d = data.get('option_d', q.option_d) or None
        q.option_e = data.get('option_e', q.option_e) or None
        q.correct_answer = data.get('correct_answer', q.correct_answer)
        q.difficulty = data.get('difficulty', q.difficulty)
        q.is_new = data.get('is_new', 'false').lower() in ('true', '1', 'on')
        q.explanation = data.get('explanation', q.explanation) or ''

        # 圖片處理
        clear_image = data.get('clear_image', 'false').lower() in ('true', '1')
        if 'question_image' in request.FILES:
            q.question_image = request.FILES['question_image']
        elif clear_image and q.question_image:
            q.question_image.delete(save=False)
            q.question_image = None

        q.save()

        return JsonResponse({'success': True})

    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)


@csrf_exempt
@require_http_methods(['POST'])
def api_delete_question(request, qid):
    """刪除題目"""
    if not request.user.is_authenticated or not request.user.is_staff:
        return JsonResponse({'error': '未授權'}, status=403)

    try:
        q = Question.objects.get(id=qid)
        # 刪除圖片檔案
        if q.question_image:
            q.question_image.delete(save=False)
        q.delete()
        return JsonResponse({'success': True})
    except Question.DoesNotExist:
        return JsonResponse({'error': '題目不存在'}, status=404)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)


@csrf_exempt
@require_http_methods(['POST'])
def api_create_question(request):
    """新增題目"""
    if not request.user.is_authenticated or not request.user.is_staff:
        return JsonResponse({'error': '未授權'}, status=403)

    try:
        data = request.POST.dict()
        q = Question.objects.create(
            chapter=data.get('chapter', ''),
            question_number=int(data.get('question_number', 1)),
            question_text=data.get('question_text', ''),
            option_a=data.get('option_a', ''),
            option_b=data.get('option_b', ''),
            option_c=data.get('option_c', ''),
            option_d=data.get('option_d') or None,
            option_e=data.get('option_e') or None,
            correct_answer=data.get('correct_answer', 'A'),
            difficulty=data.get('difficulty', 'medium'),
            is_new=data.get('is_new', 'false').lower() in ('true', '1', 'on'),
            explanation=data.get('explanation', '') or '',
        )
        if 'question_image' in request.FILES:
            q.question_image = request.FILES['question_image']
            q.save()

        return JsonResponse({'success': True, 'id': q.id})
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)


@csrf_exempt
@require_http_methods(['POST'])
def api_update_user(request, uid):
    """更新用戶資訊（Admin）— 支援身分組選擇"""
    if not request.user.is_authenticated or not request.user.is_staff:
        return JsonResponse({'error': '未授權'}, status=403)

    try:
        user = User.objects.get(id=uid)
        data = request.POST.dict()
        user.nickname = data.get('nickname', user.nickname)
        user.email = data.get('email', user.email)
        user.student_class = data.get('student_class', user.student_class) or None

        # 身分組處理
        role = data.get('role', '')
        if role == 'admin':
            user.is_superuser = True
            user.is_staff = True
            user.is_teacher = True
        elif role == 'teacher':
            user.is_superuser = False
            user.is_staff = False
            user.is_teacher = True
        elif role == 'student':
            user.is_superuser = False
            user.is_staff = False
            user.is_teacher = False
        else:
            # 相容舊版欄位
            user.is_staff = data.get('is_staff', 'false').lower() in ('true', '1', 'on')

        if data.get('password'):
            user.set_password(data.get('password'))
        user.save()
        return JsonResponse({'success': True})
    except User.DoesNotExist:
        return JsonResponse({'error': '用戶不存在'}, status=404)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)


@csrf_exempt
@require_http_methods(['POST'])
def api_create_user(request):
    """建立新用戶（支援身分組選擇）"""
    if not request.user.is_authenticated or not request.user.is_staff:
        return JsonResponse({'error': '未授權'}, status=403)

    try:
        import json as _json
        data = request.POST.dict() if request.POST else _json.loads(request.body or '{}')
        username = data.get('username', '').strip()
        password = data.get('password', '')
        email = data.get('email', '').strip()
        role = data.get('role', 'student')

        if not username:
            return JsonResponse({'error': '帳號不能為空'}, status=400)
        if not password:
            return JsonResponse({'error': '密碼不能為空'}, status=400)
        if User.objects.filter(username=username).exists():
            return JsonResponse({'error': '帳號已存在'}, status=400)

        user = User.objects.create_user(username=username, password=password, email=email)
        if role == 'admin':
            user.is_superuser = True
            user.is_staff = True
            user.is_teacher = True
        elif role == 'teacher':
            user.is_staff = False
            user.is_teacher = True
        # student: all False (default)
        user.save()
        return JsonResponse({'success': True, 'id': user.id})
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)


@csrf_exempt
@require_http_methods(['POST'])
def api_delete_user(request, uid):
    """刪除用戶"""
    if not request.user.is_authenticated or not request.user.is_staff:
        return JsonResponse({'error': '未授權'}, status=403)

    try:
        user = User.objects.get(id=uid)
        if user == request.user:
            return JsonResponse({'error': '不能刪除自己的帳號'}, status=400)
        user.delete()
        return JsonResponse({'success': True})
    except User.DoesNotExist:
        return JsonResponse({'error': '用戶不存在'}, status=404)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)


@csrf_exempt
@require_http_methods(['POST'])
def api_create_class(request):
    """批次建立班級帳號"""
    if not request.user.is_authenticated or not request.user.is_staff:
        return JsonResponse({'error': '未授權'}, status=403)

    try:
        import json as _json
        data = request.POST.dict() if request.POST else _json.loads(request.body or '{}')
        class_name = data.get('class_name', '').strip()
        count = int(data.get('count', 0))
        password = data.get('password', '')

        if not class_name:
            return JsonResponse({'error': '班級名稱不能為空'}, status=400)
        if count < 1 or count > 100:
            return JsonResponse({'error': '人數需在 1~100 之間'}, status=400)
        if not password or len(password) < 4:
            return JsonResponse({'error': '密碼至少 4 個字元'}, status=400)

        created = []
        errors = []
        for i in range(1, count + 1):
            username = f'{class_name}{i:02d}'
            if User.objects.filter(username=username).exists():
                errors.append(f'{username} 已存在')
                continue
            user = User.objects.create_user(
                username=username,
                password=password,
                student_class=class_name,
            )
            created.append(username)

        return JsonResponse({
            'success': True,
            'created': created,
            'errors': errors,
        })
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)


@csrf_exempt
@require_http_methods(['POST'])
def api_delete_class(request):
    """刪除整班帳號"""
    if not request.user.is_authenticated or not request.user.is_staff:
        return JsonResponse({'error': '未授權'}, status=403)

    try:
        import json as _json
        data = request.POST.dict() if request.POST else _json.loads(request.body or '{}')
        class_name = data.get('class_name', '').strip()

        if not class_name:
            return JsonResponse({'error': '請選擇班級'}, status=400)

        users = User.objects.filter(student_class=class_name)
        count = users.count()
        if count == 0:
            return JsonResponse({'error': f'班級 {class_name} 沒有成員'}, status=400)

        users.delete()
        return JsonResponse({'success': True, 'deleted': count})
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)


@csrf_exempt
@require_http_methods(['POST'])
def api_delete_record(request, rid):
    """刪除測驗記錄"""
    if not request.user.is_authenticated or not request.user.is_staff:
        return JsonResponse({'error': '未授權'}, status=403)

    try:
        record = QuizRecord.objects.get(id=rid)
        record.delete()
        return JsonResponse({'success': True})
    except QuizRecord.DoesNotExist:
        return JsonResponse({'error': '記錄不存在'}, status=404)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)


@csrf_exempt
@require_http_methods(['POST'])
def api_batch_delete(request):
    """批次刪除題目 / 用戶 / 記錄"""
    if not request.user.is_authenticated or not request.user.is_staff:
        return JsonResponse({'error': '未授權'}, status=403)

    try:
        data = json.loads(request.body or '{}')
        delete_type = data.get('type', '')
        ids = data.get('ids', [])

        if not isinstance(ids, list) or not ids:
            return JsonResponse({'error': '請選擇至少一個項目'}, status=400)

        if delete_type == 'question':
            Question.objects.filter(id__in=ids).delete()
        elif delete_type == 'user':
            # 不能刪除自己
            my_id = request.user.id
            safe_ids = [i for i in ids if i != my_id]
            if not safe_ids:
                return JsonResponse({'error': '不能刪除自己的帳號'}, status=400)
            User.objects.filter(id__in=safe_ids).delete()
        elif delete_type == 'record':
            QuizRecord.objects.filter(id__in=ids).delete()
        else:
            return JsonResponse({'error': '未知類型'}, status=400)

        return JsonResponse({'success': True, 'deleted': len(ids)})
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)


@csrf_exempt
@require_http_methods(['POST'])
def api_update_profile(request):
    """使用者自行更新個人資料（暱稱、Email）"""
    if not request.user.is_authenticated:
        return JsonResponse({'error': '請先登入'}, status=401)

    try:
        data = request.POST.dict()
        if 'nickname' in data:
            request.user.nickname = data['nickname']
        if 'email' in data:
            request.user.email = data['email']
        request.user.save()
        return JsonResponse({'success': True})
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)


@csrf_exempt
@require_http_methods(['POST'])
def api_change_password(request):
    """使用者自行更改密碼"""
    if not request.user.is_authenticated:
        return JsonResponse({'error': '請先登入'}, status=401)

    try:
        import json as _json
        data = request.POST.dict() if request.POST else _json.loads(request.body or '{}')
        old_password = data.get('old_password', '')
        new_password = data.get('new_password', '')

        if not old_password or not new_password:
            return JsonResponse({'error': '請填入舊密碼與新密碼'}, status=400)
        if len(new_password) < 3:
            return JsonResponse({'error': '新密碼至少 3 個字元'}, status=400)
        if not request.user.check_password(old_password):
            return JsonResponse({'error': '舊密碼錯誤'}, status=400)

        request.user.set_password(new_password)
        request.user.save()
        from django.contrib.auth import update_session_auth_hash
        update_session_auth_hash(request, request.user)
        return JsonResponse({'success': True})
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)


@csrf_exempt
@require_http_methods(['POST'])
def api_delete_account(request):
    """使用者自行刪除自己的帳號"""
    if not request.user.is_authenticated:
        return JsonResponse({'error': '請先登入'}, status=401)

    try:
        data = request.POST.dict() if request.POST else {}
        confirm = data.get('confirm', '')
        if confirm != 'DELETE':
            return JsonResponse({'error': '請輸入 DELETE 確認刪除'}, status=400)

        user = request.user
        from django.contrib.auth import logout
        logout(request)
        user.delete()
        return JsonResponse({'success': True})
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)


@require_http_methods(['GET'])
def api_stats_overview(request):
    """資訊面板：概觀統計（帳號數、上線人數、答題次數、框架、章節數、自編題目）"""
    if not request.user.is_authenticated or not request.user.is_staff:
        return JsonResponse({'error': '未授權'}, status=403)

    try:
        total_users = User.objects.count()
        total_quiz_attempts = QuizRecord.objects.count()

        # 更新管理員自己的 last_login，讓上線人數即時反映
        User.objects.filter(id=request.user.id).update(last_login=timezone.now())
        cutoff = timezone.now() - timedelta(minutes=15)
        online_users = User.objects.filter(last_login__gte=cutoff).count()

        # 各章節答題次數（豎狀圖用）
        chapter_attempts = list(
            QuizRecord.objects.values('chapter')
            .annotate(count=models.Count('id'))
            .order_by('-count')
        )

        # 新增資料：章節數、自編題目數
        raw_chapters = list(Question.objects.values_list('chapter', flat=True))
        total_chapters = len(set(raw_chapters))
        total_new_questions = Question.objects.filter(is_new=True).count()
        framework = 'Django ' + '.'.join(str(v) for v in __import__('django').VERSION[:2])

        return JsonResponse({
            'success': True,
            'total_users': total_users,
            'online_users': online_users,
            'total_quiz_attempts': total_quiz_attempts,
            'chapter_attempts': chapter_attempts,
            'total_chapters': total_chapters,
            'total_new_questions': total_new_questions,
            'framework': framework,
        })
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)


@require_http_methods(['GET'])
def api_user_error_stats(request):
    """資訊面板：指定使用者的答題統計與錯誤率"""
    if not request.user.is_authenticated or not request.user.is_staff:
        return JsonResponse({'error': '未授權'}, status=403)

    uid = request.GET.get('user_id')
    if not uid:
        return JsonResponse({'error': '請指定使用者'}, status=400)

    try:
        user = User.objects.get(id=uid)
    except User.DoesNotExist:
        return JsonResponse({'error': '使用者不存在'}, status=404)

    records = QuizRecord.objects.filter(user=user)
    total_answered = 0
    total_correct = 0
    for r in records:
        total_answered += r.total_questions
        total_correct += r.correct_count

    total_wrong = total_answered - total_correct
    error_rate = round((total_wrong / total_answered * 100), 1) if total_answered > 0 else 0

    # 各次測驗分數（豎狀圖用）
    quiz_scores = list(
        records.values('id', 'score', 'correct_count', 'total_questions',
                       'chapter', 'created_at').order_by('-created_at')[:20]
    )
    # 整理時間格式
    for qs in quiz_scores:
        qs['date'] = qs['created_at'].strftime('%m/%d') if qs['created_at'] else ''
        qs['score'] = round(qs['score'], 1)
        del qs['created_at']

    wrong_dist = (WrongAnswer.objects.filter(quiz_record__user=user)
                  .values('question_id', 'question__question_text', 'question__chapter')
                  .annotate(count=models.Count('id')).order_by('-count')[:30])

    return JsonResponse({
        'success': True,
        'user': {
            'id': user.id,
            'username': user.username,
            'nickname': user.nickname or user.username,
        },
        'stats': {
            'total_answered': total_answered,
            'total_correct': total_correct,
            'total_wrong': total_wrong,
            'error_rate': error_rate,
            'quiz_count': records.count(),
        },
        'quiz_scores': quiz_scores,
        'wrong_distribution': list(wrong_dist),
    })


@require_http_methods(['GET'])
def api_question_error_stats(request):
    """資訊面板：指定題目的錯誤率與選項分布"""
    if not request.user.is_authenticated or not request.user.is_staff:
        return JsonResponse({'error': '未授權'}, status=403)

    qid = request.GET.get('question_id')
    if not qid:
        return JsonResponse({'error': '請指定題目'}, status=400)

    try:
        question = Question.objects.get(id=qid)
    except Question.DoesNotExist:
        return JsonResponse({'error': '題目不存在'}, status=404)

    wrong_count = WrongAnswer.objects.filter(question=question).count()
    wrong_records_ids = (WrongAnswer.objects.filter(question=question)
                         .values_list('quiz_record_id', flat=True).distinct())

    # 嘗試估算總答題次數：每個有這題錯題的 record 代表這題被答過
    # 再加上可能有答對但沒在 WrongAnswer 中的 record
    # 用所有包含相同題數+章節的 record 來估算
    wrong_record_set = set(wrong_records_ids)
    # 從該章節的 QuizRecord 中估計出現次數
    same_chapter_records = QuizRecord.objects.filter(chapter=question.chapter)
    total_approx = len(wrong_record_set)
    # 再加上可能有答對但沒記錄的估算
    if same_chapter_records.count() > 0:
        # 保守估算：至少有 wrong_record_set 個，最多 same_chapter_records 個
        total_approx = max(total_approx, len(wrong_record_set))

    error_rate = round((wrong_count / max(total_approx, 1)) * 100, 1)

    # 選項分布（包含正解統計）
    option_dist = {}
    wrong_answers = (WrongAnswer.objects.filter(question=question)
                     .values('user_answer').annotate(count=models.Count('id')))
    for wa in wrong_answers:
        option_dist[wa['user_answer']] = wa['count']

    # 正解次數估算 = 總嘗試次數 - 答錯次數
    correct_approx = max(total_approx - wrong_count, 0)

    options = {
        'A': question.option_a or '',
        'B': question.option_b or '',
        'C': question.option_c or '',
        'D': question.option_d or '',
        'E': question.option_e or '',
    }

    return JsonResponse({
        'success': True,
        'question': {
            'id': question.id,
            'chapter': question.chapter,
            'number': question.question_number,
            'text': question.question_text,
            'correct_answer': question.correct_answer,
            'options': options,
        },
        'error_stats': {
            'wrong_count': wrong_count,
            'correct_approx': correct_approx,
            'total_attempts_approx': total_approx,
            'error_rate': error_rate,
        },
        'option_distribution': option_dist,
    })


# ═══════════════════════════════════════════
#   Feature 1: 學習數據與圖表分析 API
# ═══════════════════════════════════════════

@require_http_methods(['GET'])
def api_my_chapter_stats(request):
    """回傳當前使用者在各章節的答對率（Chart.js 雷達圖用）"""
    if not request.user.is_authenticated:
        return JsonResponse({'error': '請先登入'}, status=401)

    records = QuizRecord.objects.filter(user=request.user, is_sr=False)
    chapter_data = {}
    for r in records:
        ch = r.chapter
        if ch not in chapter_data:
            chapter_data[ch] = {'total': 0, 'correct': 0}
        chapter_data[ch]['total'] += r.total_questions
        chapter_data[ch]['correct'] += r.correct_count

    labels = []
    rates = []
    for ch in sorted(chapter_data.keys()):
        d = chapter_data[ch]
        rate = round(d['correct'] / d['total'] * 100, 1) if d['total'] > 0 else 0
        labels.append(ch)
        rates.append(rate)

    return JsonResponse({
        'success': True,
        'labels': labels,
        'rates': rates,
        'total_quiz_count': records.count(),
    })


@require_http_methods(['GET'])
def api_quiz_timeline(request):
    """回傳使用者的分數趨勢（折線圖用）"""
    if not request.user.is_authenticated:
        return JsonResponse({'error': '請先登入'}, status=401)

    records = QuizRecord.objects.filter(user=request.user).order_by('created_at')[:30]
    data = []
    for r in records:
        data.append({
            'id': r.id,
            'chapter': r.chapter,
            'score': round(r.score, 1),
            'date': r.created_at.strftime('%m/%d %H:%M'),
            'sr': r.is_sr,
        })
    return JsonResponse({'success': True, 'records': data})


@require_http_methods(['GET'])
def api_boss_questions(request):
    """回傳魔王題（錯誤率 >= 70%）列表"""
    if not request.user.is_authenticated or not request.user.is_staff:
        return JsonResponse({'error': '未授權'}, status=403)

    questions = Question.objects.filter(total_attempt_count__gte=5)
    boss_list = []
    for q in questions:
        err_rate = q.error_rate
        if err_rate >= 70:
            boss_list.append({
                'id': q.id,
                'chapter': q.chapter,
                'number': q.question_number,
                'text': q.question_text[:80],
                'error_rate': err_rate,
                'error_count': q.error_count,
                'total_attempts': q.total_attempt_count,
            })
    boss_list.sort(key=lambda x: x['error_rate'], reverse=True)

    return JsonResponse({
        'success': True,
        'boss_questions': boss_list,
        'total_boss': len(boss_list),
    })


# ═══════════════════════════════════════════
#   Feature 2: CSV 批次匯入/匯出
# ═══════════════════════════════════════════

@require_http_methods(['GET'])
def export_questions_csv(request):
    """匯出題庫 CSV"""
    if not request.user.is_authenticated or not request.user.is_staff:
        return JsonResponse({'error': '未授權'}, status=403)

    import csv, io
    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(['章節', '題號', '題目內容', '選項A', '選項B', '選項C', '選項D', '選項E', '正確答案', '難易度', '詳解'])

    questions = Question.objects.all().order_by('chapter', 'question_number')
    for q in questions:
        writer.writerow([
            q.chapter, q.question_number, q.question_text,
            q.option_a, q.option_b, q.option_c,
            q.option_d or '', q.option_e or '',
            q.correct_answer, q.difficulty, q.explanation or '',
        ])

    csv_bytes = output.getvalue().encode('utf-8-sig')
    from django.http import HttpResponse
    response = HttpResponse(csv_bytes, content_type='text/csv; charset=utf-8-sig')
    response['Content-Disposition'] = 'attachment; filename="quiz_questions_export.csv"'
    return response


@csrf_exempt
@require_http_methods(['POST'])
def import_questions_csv(request):
    """批次匯入題庫 CSV"""
    if not request.user.is_authenticated or not request.user.is_staff:
        return JsonResponse({'error': '未授權'}, status=403)

    if 'csv_file' not in request.FILES:
        return JsonResponse({'error': '請上傳 CSV 檔案'}, status=400)

    import csv, io
    csv_file = request.FILES['csv_file']
    decoded = csv_file.read().decode('utf-8-sig')
    reader = csv.DictReader(io.StringIO(decoded))

    created = 0
    errors = []
    overwrite = request.POST.get('overwrite', 'false').lower() == 'true'

    for row_num, row in enumerate(reader, start=2):
        chapter = row.get('章節', '').strip()
        qnum_str = row.get('題號', '').strip()

        if not chapter or not qnum_str:
            errors.append(f'第 {row_num} 行：章節或題號為空')
            continue

        try:
            qnum = int(qnum_str)
        except ValueError:
            errors.append(f'第 {row_num} 行：題號格式錯誤')
            continue

        question_text = row.get('題目內容', '').strip()
        if not question_text:
            errors.append(f'第 {row_num} 行：題目內容為空')
            continue

        existing = Question.objects.filter(chapter=chapter, question_number=qnum).first()
        if existing:
            if not overwrite:
                errors.append(f'第 {row_num} 行：題目 [{chapter}-{qnum}] 已存在（略過）')
                continue
            # 覆寫模式
            existing.question_text = question_text
            existing.option_a = row.get('選項A', '').strip()
            existing.option_b = row.get('選項B', '').strip()
            existing.option_c = row.get('選項C', '').strip()
            existing.option_d = row.get('選項D', '').strip() or None
            existing.option_e = row.get('選項E', '').strip() or None
            existing.correct_answer = row.get('正確答案', 'A').strip().upper()
            existing.difficulty = row.get('難易度', 'medium').strip()
            existing.explanation = row.get('詳解', '').strip() or ''
            existing.save()
            created += 1
        else:
            Question.objects.create(
                chapter=chapter,
                question_number=qnum,
                question_text=question_text,
                option_a=row.get('選項A', '').strip(),
                option_b=row.get('選項B', '').strip(),
                option_c=row.get('選項C', '').strip(),
                option_d=row.get('選項D', '').strip() or None,
                option_e=row.get('選項E', '').strip() or None,
                correct_answer=row.get('正確答案', 'A').strip().upper(),
                difficulty=row.get('難易度', 'medium').strip(),
                explanation=row.get('詳解', '').strip() or '',
            )
            created += 1

    return JsonResponse({
        'success': True,
        'created': created,
        'errors': errors,
    })


# ═══════════════════════════════════════════
#   Feature 3: 課程與群組功能
# ═══════════════════════════════════════════

def classroom_list(request):
    """教師的課程列表頁面"""
    if not request.user.is_authenticated or not request.user.is_teacher:
        return redirect('home')

    classrooms = Classroom.objects.filter(teacher=request.user).order_by('-created_at')
    return render(request, 'quiz_app/classroom_list.html', {
        'classrooms': classrooms,
    })


def classroom_detail(request, classroom_id):
    """課程儀表板 — 教師檢視學生表現"""
    if not request.user.is_authenticated or not request.user.is_teacher:
        return redirect('home')

    try:
        classroom = Classroom.objects.get(id=classroom_id, teacher=request.user)
    except Classroom.DoesNotExist:
        return redirect('classroom_list')

    enrollments = classroom.enrollments.select_related('student').all()
    students_data = []
    for enroll in enrollments:
        student = enroll.student
        records = QuizRecord.objects.filter(user=student)
        total_quiz = records.count()
        total_correct = sum(r.correct_count for r in records)
        total_qs = sum(r.total_questions for r in records)
        avg_score = round(records.aggregate(avg=models.Avg('score'))['avg'] or 0, 1) if total_quiz > 0 else 0
        students_data.append({
            'id': student.id,
            'nickname': student.nickname or student.username,
            'total_quiz': total_quiz,
            'avg_score': avg_score,
            'total_correct': total_correct,
            'total_questions': total_qs,
        })

    # 全班常見錯題 TOP 10
    student_ids = [enroll.student.id for enroll in enrollments]
    from django.db.models import Count
    common_wrongs = (WrongAnswer.objects
                     .filter(quiz_record__user_id__in=student_ids)
                     .values('question_id', 'question__question_text', 'question__chapter')
                     .annotate(wrong_count=Count('id'))
                     .order_by('-wrong_count')[:10])

    return render(request, 'quiz_app/classroom_detail.html', {
        'classroom': classroom,
        'students': students_data,
        'common_wrongs': list(common_wrongs),
    })


@csrf_exempt
@require_http_methods(['POST'])
def api_classroom_create(request):
    """教師建立課程"""
    if not request.user.is_authenticated or not request.user.is_teacher:
        return JsonResponse({'error': '未授權'}, status=403)

    try:
        data = json.loads(request.body or '{}')
        name = data.get('name', '').strip()
        description = data.get('description', '').strip()

        if not name:
            return JsonResponse({'error': '請輸入課程名稱'}, status=400)

        # 產生唯一邀請碼
        import string, random
        while True:
            code = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
            if not Classroom.objects.filter(invite_code=code).exists():
                break

        classroom = Classroom.objects.create(
            name=name,
            teacher=request.user,
            invite_code=code,
            description=description,
        )
        return JsonResponse({'success': True, 'id': classroom.id, 'invite_code': code})
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)


@csrf_exempt
@require_http_methods(['POST'])
def api_classroom_join(request):
    """學生透過邀請碼加入課程"""
    if not request.user.is_authenticated:
        return JsonResponse({'error': '請先登入'}, status=401)

    try:
        data = json.loads(request.body or '{}')
        code = data.get('invite_code', '').strip().upper()

        if not code:
            return JsonResponse({'error': '請輸入邀請碼'}, status=400)

        try:
            classroom = Classroom.objects.get(invite_code=code, is_active=True)
        except Classroom.DoesNotExist:
            return JsonResponse({'error': '邀請碼無效或課程已關閉'}, status=400)

        # 檢查是否已經加入
        if ClassroomEnrollment.objects.filter(classroom=classroom, student=request.user).exists():
            return JsonResponse({'error': '你已加入此課程'}, status=400)

        # 教師不能加入自己的課程
        if classroom.teacher == request.user:
            return JsonResponse({'error': '教師無需加入自己的課程'}, status=400)

        ClassroomEnrollment.objects.create(classroom=classroom, student=request.user)

        return JsonResponse({
            'success': True,
            'classroom_name': classroom.name,
            'classroom_id': classroom.id,
        })
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)


def classroom_my(request):
    """學生的已加入課程頁面"""
    if not request.user.is_authenticated:
        return redirect('login')

    enrollments = ClassroomEnrollment.objects.filter(student=request.user).select_related('classroom', 'classroom__teacher')
    return render(request, 'quiz_app/classroom_my.html', {
        'enrollments': enrollments,
    })


@csrf_exempt
@require_http_methods(['POST'])
def api_classroom_leave(request):
    """學生退出課程"""
    if not request.user.is_authenticated:
        return JsonResponse({'error': '請先登入'}, status=401)
    try:
        data = json.loads(request.body or '{}')
        classroom_id = data.get('classroom_id')
        enrollment = ClassroomEnrollment.objects.filter(
            classroom_id=classroom_id, student=request.user
        ).first()
        if not enrollment:
            return JsonResponse({'error': '你不在這個課程中'}, status=400)
        enrollment.delete()
        return JsonResponse({'success': True})
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)


@csrf_exempt
@require_http_methods(['POST'])
def api_classroom_kick(request, classroom_id):
    """教師踢除學生"""
    if not request.user.is_authenticated or not request.user.is_teacher:
        return JsonResponse({'error': '未授權'}, status=403)
    try:
        classroom = Classroom.objects.get(id=classroom_id, teacher=request.user)
        data = json.loads(request.body or '{}')
        student_id = data.get('student_id')
        if not student_id:
            return JsonResponse({'error': '請指定學生'}, status=400)
        enrollment = ClassroomEnrollment.objects.filter(
            classroom=classroom, student_id=student_id
        ).first()
        if not enrollment:
            return JsonResponse({'error': '該學生不在課程中'}, status=400)
        enrollment.delete()
        return JsonResponse({'success': True})
    except Classroom.DoesNotExist:
        return JsonResponse({'error': '課程不存在'}, status=404)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)


@csrf_exempt
@require_http_methods(['POST'])
def api_classroom_close(request, classroom_id):
    """教師關閉課程（軟刪除，設為不啟用）"""
    if not request.user.is_authenticated or not request.user.is_teacher:
        return JsonResponse({'error': '未授權'}, status=403)
    try:
        classroom = Classroom.objects.get(id=classroom_id, teacher=request.user)
        classroom.is_active = False
        classroom.save(update_fields=['is_active'])
        return JsonResponse({'success': True})
    except Classroom.DoesNotExist:
        return JsonResponse({'error': '課程不存在'}, status=404)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)


@csrf_exempt
@require_http_methods(['POST'])
def api_classroom_delete(request, classroom_id):
    """教師刪除課程（永久刪除）"""
    if not request.user.is_authenticated or not request.user.is_teacher:
        return JsonResponse({'error': '未授權'}, status=403)
    try:
        classroom = Classroom.objects.get(id=classroom_id, teacher=request.user)
        # 刪除所有成員關係
        ClassroomEnrollment.objects.filter(classroom=classroom).delete()
        classroom.delete()
        return JsonResponse({'success': True})
    except Classroom.DoesNotExist:
        return JsonResponse({'error': '課程不存在'}, status=404)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)


# ═══════════════════════════════════════════
#   Feature 4: PDF 報表匯出
# ═══════════════════════════════════════════

def export_quiz_pdf(request):
    """生成使用者的學習歷程 PDF 報表"""
    if not request.user.is_authenticated:
        return redirect('login')

    from django.template.loader import render_to_string
    from django.conf import settings
    import os

    user = request.user

    # 統計資料
    records = QuizRecord.objects.filter(user=user).order_by('-created_at')
    total_quiz = records.count()
    total_qs = sum(r.total_questions for r in records)
    total_correct = sum(r.correct_count for r in records)
    avg_score = round(records.aggregate(avg=models.Avg('score'))['avg'] or 0, 1) if total_quiz > 0 else 0

    # 各章節統計
    chapter_stats = {}
    for r in records:
        ch = r.chapter
        if ch not in chapter_stats:
            chapter_stats[ch] = {'total': 0, 'correct': 0}
        chapter_stats[ch]['total'] += r.total_questions
        chapter_stats[ch]['correct'] += r.correct_count

    chapters_data = []
    for ch in sorted(chapter_stats.keys()):
        d = chapter_stats[ch]
        rate = round(d['correct'] / d['total'] * 100, 1) if d['total'] > 0 else 0
        chapters_data.append({'name': ch, 'rate': rate, 'correct': d['correct'], 'total': d['total']})

    # 錯題統計
    wrong_qs = WrongAnswer.objects.filter(quiz_record__user=user).count()

    html = render_to_string('quiz_app/pdf_report.html', {
        'user': user,
        'total_quiz': total_quiz,
        'total_questions': total_qs,
        'total_correct': total_correct,
        'total_wrong': wrong_qs,
        'avg_score': avg_score,
        'chapters': chapters_data,
        'generated_at': timezone.now().strftime('%Y-%m-%d %H:%M'),
    })

    try:
        # 使用 reportlab 直接產生 PDF（純 Python，無需外部依賴）
        from io import BytesIO
        from django.http import HttpResponse
        from reportlab.lib import colors
        from reportlab.lib.pagesizes import A4
        from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
        from reportlab.lib.units import cm, mm
        from reportlab.platypus import (
            SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
            PageBreak
        )
        from reportlab.pdfbase import pdfmetrics
        from reportlab.pdfbase.ttfonts import TTFont

        pdf_file = BytesIO()
        doc = SimpleDocTemplate(
            pdf_file, pagesize=A4,
            topMargin=2*cm, bottomMargin=2*cm,
            leftMargin=1.5*cm, rightMargin=1.5*cm,
        )

        styles = getSampleStyleSheet()
        title_style = ParagraphStyle(
            'CustomTitle', parent=styles['Title'],
            fontSize=24, leading=30, spaceAfter=12,
            textColor=colors.HexColor('#0a0a23'),
        )
        subtitle_style = ParagraphStyle(
            'Subtitle', parent=styles['Normal'],
            fontSize=14, leading=18, spaceAfter=6,
            textColor=colors.HexColor('#64748b'),
        )
        heading_style = ParagraphStyle(
            'Heading2', parent=styles['Heading2'],
            fontSize=16, leading=20, spaceAfter=10,
            spaceBefore=20,
            textColor=colors.HexColor('#0a0a23'),
        )
        normal_style = ParagraphStyle(
            'CustomNormal', parent=styles['Normal'],
            fontSize=11, leading=16,
            textColor=colors.HexColor('#1a1a2e'),
        )
        stats_style = ParagraphStyle(
            'StatsValue', parent=styles['Normal'],
            fontSize=22, leading=26, spaceAfter=2,
            textColor=colors.HexColor('#00d4ff'),
            alignment=1,  # center
        )
        stats_label = ParagraphStyle(
            'StatsLabel', parent=styles['Normal'],
            fontSize=9, leading=12,
            textColor=colors.HexColor('#64748b'),
            alignment=1,
        )

        story = []

        # ── Header ──
        story.append(Paragraph('📊 學習歷程報告', title_style))
        story.append(Paragraph('資料結構測驗 — 學習總覽', subtitle_style))
        story.append(Spacer(1, 6))
        user_info = f'👤 {user.nickname or user.username}'
        if user.student_class:
            user_info += f'&nbsp;&nbsp;🏫 {user.student_class}'
        story.append(Paragraph(user_info, normal_style))
        story.append(Spacer(1, 20))

        # ── Stats Overview ──
        story.append(Paragraph('📈 學習總覽', heading_style))
        stats_data = [
            [str(total_quiz), str(total_questions), str(total_correct), str(wrong_qs), f'{avg_score}'],
            ['測驗次數', '總答題數', '總正確數', '總錯誤數', '平均分數'],
        ]
        stats_table = Table(stats_data, colWidths=[3.2*cm]*5)
        stats_table.setStyle(TableStyle([
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTSIZE', (0, 0), (-1, 0), 22),
            ('FONTSIZE', (0, 1), (-1, 1), 9),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.HexColor('#0a0a23')),
            ('TEXTCOLOR', (0, 1), (-1, 1), colors.HexColor('#64748b')),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 4),
            ('TOPPADDING', (0, 1), (-1, 1), 4),
            ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor('#f0f4ff')),
            ('BOX', (0, 0), (-1, -1), 0.5, colors.HexColor('#e2e8f0')),
            ('INNERGRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#e2e8f0')),
        ]))
        story.append(stats_table)
        story.append(Spacer(1, 24))

        # ── Chapter Performance ──
        story.append(Paragraph('📚 各章節表現', heading_style))

        chapter_header = [['章節', '答對', '總題數', '正確率']]
        chapter_rows = [chapter_header]
        for ch in chapters_data:
            rate_color = '#00e676' if ch['rate'] >= 80 else '#ffd93d' if ch['rate'] >= 60 else '#ff6b6b'
            chapter_rows.append([
                ch['name'],
                str(ch['correct']),
                str(ch['total']),
                f'{ch["rate"]}%',
            ])

        chapter_table = Table(chapter_rows, colWidths=[8*cm, 2.5*cm, 2.5*cm, 3*cm])
        chapter_table.setStyle(TableStyle([
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('ALIGN', (0, 0), (0, -1), 'LEFT'),
            ('FONTSIZE', (0, 0), (-1, 0), 11),
            ('FONTSIZE', (0, 1), (-1, -1), 10),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#0a0a23')),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 8),
            ('TOPPADDING', (0, 0), (-1, 0), 8),
            ('BOTTOMPADDING', (0, 1), (-1, -1), 6),
            ('TOPPADDING', (0, 1), (-1, -1), 6),
            ('BOX', (0, 0), (-1, -1), 0.5, colors.HexColor('#e2e8f0')),
            ('INNERGRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#e2e8f0')),
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#f8fafc')]),
        ]))
        chapter_table.hAlign = 'LEFT'
        story.append(chapter_table)
        story.append(Spacer(1, 24))

        # ── Footer ──
        story.append(Spacer(1, 20))
        footer_text = f'資料結構測驗網站 · 報告產生時間：{timezone.now().strftime("%Y-%m-%d %H:%M")} · 此報告為系統自動生成'
        story.append(Paragraph(footer_text, ParagraphStyle(
            'Footer', parent=styles['Normal'],
            fontSize=8, textColor=colors.HexColor('#94a3b8'),
            alignment=1, spaceBefore=10,
        )))

        doc.build(story)
        pdf_file.seek(0)
        response = HttpResponse(pdf_file.read(), content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="learning_report_{user.username}_{timezone.now().strftime("%Y%m%d")}.pdf"'
        return response
    except Exception as e:
        # 若 PDF 產生失敗（極少情況），回傳 HTML 預覽
        return render(request, 'quiz_app/pdf_report.html', {
            'user': user,
            'total_quiz': total_quiz,
            'total_questions': total_qs,
            'total_correct': total_correct,
            'total_wrong': wrong_qs,
            'avg_score': avg_score,
            'chapters': chapters_data,
            'generated_at': timezone.now().strftime('%Y-%m-%d %H:%M'),
        })