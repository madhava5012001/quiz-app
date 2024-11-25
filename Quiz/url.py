from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('login', views.login, name='login'),
    path('user-home', views.user_home, name='user-home'),
    path('register', views.register, name='register'),
    path('logout', views.logout, name='logout'),
    path('leaderboard', views.leaderboard, name='leaderboard'),
    path('submission-result/(?P<attempted_question_pk>\d+)', views.submission_result, name='submission-result')
]