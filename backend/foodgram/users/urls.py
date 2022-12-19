""" Спринт 14 Проект «Продуктовый помощник»  
Автор: Фредди Андрес Парра
Студент факультета Бэкенд. Когорта 14+

Имя файла: urls.py
Описание файла: записывает все адреса в приложении: users
Переменные:
 - urlpatterns: список адресов
"""
from django.contrib.auth.views import LogoutView
from django.contrib.auth.views import LoginView
from django.contrib.auth.views import PasswordChangeView
from django.contrib.auth.views import PasswordChangeDoneView
from django.contrib.auth.views import PasswordResetView
from django.contrib.auth.views import PasswordResetConfirmView
from django.contrib.auth.views import PasswordResetCompleteView
from django.contrib.auth.views import PasswordResetDoneView

from django.urls import path, reverse_lazy

from . import views


app_name = 'users'


urlpatterns = [
    # 
    path('signup/', views.SignUp.as_view(), name='signup'),
    #
    path('login', LoginView.as_view(
        template_name='users/login.html'),
        name='login'),
    # 
    path('logout/', LogoutView.as_view(
        template_name='users/logged_out.html'),
        name='logout'),
    #
    path('password_change/', PasswordChangeView.as_view( 
         template_name='users/password_change_form.html', 
         success_url=reverse_lazy('users:password_change_done')), 
         name='password_change_form'),
    #
    path('password_change/done/', PasswordChangeDoneView.as_view(
        template_name='users/password_change_done.html'),
        name='password_change_done'),
    #
    path('password_reset/', PasswordResetView.as_view(
        template_name='users/password_reset_form.html',
        success_url=reverse_lazy('users:password_reset_done')),
        name='password_reset_form'),
    #
    path('password_reset/done/', PasswordResetDoneView.as_view(
        template_name='users/password_reset_done.html'),
        name='password_reset_done'),
    #
    path('reset/<uidb64>/<token>/', PasswordResetConfirmView.as_view(
        template_name='users/password_reset_confirm.html',
        success_url=reverse_lazy('users:password_reset_complete')),
        name='password_reset_confirm'),
    #
    path('reset/done/', PasswordResetCompleteView.as_view(
        template_name='users/password_reset_complete.html'),
        name='password_reset_complete'),
]