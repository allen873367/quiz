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
    path('api/profile/update/', views.api_update_profile, name='api_update_profile'),
    path('api/profile/change-password/', views.api_change_password, name='api_change_password'),
    path('api/profile/delete/', views.api_delete_account, name='api_delete_account'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)