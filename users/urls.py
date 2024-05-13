from . import views
from django.urls import path
from django.contrib.auth import views as auth_views
from .forms import CustomPasswordResetForm

urlpatterns = [
    path('login/', views.login, name='login'),
    path('register/', views.register, name='register'),
    path('change/password/', views.change_password, name='change_password'),
    path('logout/', views.user_logout, name='logout'),
    # pass resets...

    path('password_reset/', auth_views.PasswordResetView.as_view(
        form_class=CustomPasswordResetForm,
        template_name='auth/pass_reset/password_reset_form.html',
        email_template_name='auth/pass_reset/password_reset_email.html',
        subject_template_name='auth/pass_reset/password_reset_subject.txt'
    ), name='password_reset'),

    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(
        template_name='auth/pass_reset/password_reset_done.html'
    ), name='password_reset_done'),

    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(
        template_name='auth/pass_reset/password_reset_confirm.html'
    ), name='password_reset_confirm'),

    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(
        template_name='auth/pass_reset/password_reset_complete.html'
    ), name='password_reset_complete'),
    

    path('dashboard/', views.dashboard, name='dashboard'),
    path('profile/', views.profile, name='profile'),
    # path('chat/', views.chat, name='chat'),
    # path('my_favorites/', views.my_favorites, name='my_favorites'),
    path('view/order/<int:pk>/', views.view_order, name='view_order'),

]

