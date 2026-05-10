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
    path('random-quiz/', views.random_quiz, name='random_quiz'),
    path('submit/', views.submit_quiz, name='submit_quiz'),
    path('leaderboard/', views.leaderboard, name='leaderboard'),
    path('wrong-answers/', views.wrong_answers, name='wrong_answers'),
    path('wrong-answers/<int:record_id>/', views.wrong_answers_detail, name='wrong_answers_detail'),
    path('review-wrong/<int:wrong_id>/', views.review_wrong, name='review_wrong'),
    path('quiz-records/', views.quiz_records, name='quiz_records'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)