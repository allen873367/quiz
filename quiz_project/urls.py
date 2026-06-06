from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from quiz_app import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.quiz_home, name='home'),
    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('logout/', views.logout_view, name='logout'),
    path('quiz/<str:chapter>/', views.start_quiz, name='start_quiz'),
    path('quiz/<str:chapter>/take/', views.take_quiz, name='take_quiz'),
    path('random-quiz/', views.random_quiz, name='random_quiz'),
    path('random-quiz/setup/', views.random_quiz_setup, name='random_quiz_setup'),
    path('random-quiz/take/', views.take_random_quiz, name='take_random_quiz'),
    path('submit/', views.submit_quiz, name='submit_quiz'),
    path('leaderboard/', views.leaderboard, name='leaderboard'),
    path('leaderboard/sr/', views.sr_leaderboard, name='sr_leaderboard'),
    path('wrong-answers/', views.wrong_answers, name='wrong_answers'),
    path('wrong-answers/<int:record_id>/', views.wrong_answers_detail, name='wrong_answers_detail'),
    path('review-wrong/<int:wrong_id>/', views.review_wrong, name='review_wrong'),
    path('quiz-records/', views.quiz_records, name='quiz_records'),
    path('admin-panel/', views.admin_panel, name='admin_panel'),
    path('admin-panel/api/question/<int:qid>/', views.api_get_question, name='api_get_question'),
    path('admin-panel/api/question/<int:qid>/update/', views.api_update_question, name='api_update_question'),
    path('admin-panel/api/question/<int:qid>/delete/', views.api_delete_question, name='api_delete_question'),
    path('admin-panel/api/question/create/', views.api_create_question, name='api_create_question'),
    path('admin-panel/api/user/<int:uid>/update/', views.api_update_user, name='api_update_user'),
    path('admin-panel/api/user/<int:uid>/delete/', views.api_delete_user, name='api_delete_user'),
    path('admin-panel/api/user/create/', views.api_create_user, name='api_create_user'),
    path('admin-panel/api/record/<int:rid>/delete/', views.api_delete_record, name='api_delete_record'),
    path('admin-panel/api/batch-delete/', views.api_batch_delete, name='api_batch_delete'),
    path('admin-panel/api/class/create/', views.api_create_class, name='api_create_class'),
    path('admin-panel/api/class/delete/', views.api_delete_class, name='api_delete_class'),
    path('api/profile/update/', views.api_update_profile, name='api_update_profile'),
    path('api/profile/change-password/', views.api_change_password, name='api_change_password'),
    path('api/profile/delete/', views.api_delete_account, name='api_delete_account'),
    path('admin-panel/api/stats/overview/', views.api_stats_overview, name='api_stats_overview'),
    path('admin-panel/api/stats/user-errors/', views.api_user_error_stats, name='api_user_error_stats'),
    path('admin-panel/api/stats/question-errors/', views.api_question_error_stats, name='api_question_error_stats'),

    # ─── Feature 1: 圖表分析 ───
    path('api/my-chapter-stats/', views.api_my_chapter_stats, name='api_my_chapter_stats'),
    path('api/quiz-timeline/', views.api_quiz_timeline, name='api_quiz_timeline'),
    path('admin-panel/api/stats/boss-questions/', views.api_boss_questions, name='api_boss_questions'),

    # ─── Feature 2: CSV 匯入/匯出 ───
    path('admin-panel/export/csv/', views.export_questions_csv, name='export_questions_csv'),
    path('admin-panel/import/csv/', views.import_questions_csv, name='import_questions_csv'),

    # ─── Feature 3: 班級功能 ───
    path('classroom/', views.classroom_list, name='classroom_list'),
    path('classroom/<int:classroom_id>/', views.classroom_detail, name='classroom_detail'),
    path('classroom/my/', views.classroom_my, name='classroom_my'),
    path('api/classroom/create/', views.api_classroom_create, name='api_classroom_create'),
    path('api/classroom/join/', views.api_classroom_join, name='api_classroom_join'),

    # ─── Feature 4: PDF 匯出 ───
    path('export/pdf/', views.export_quiz_pdf, name='export_quiz_pdf'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)