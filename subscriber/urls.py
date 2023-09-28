from django.urls import path
from . import views


urlpatterns = [

    path('', views.user_login, name='login'),
    path('register/', views.user_registration, name='register'),
    path('logout/', views.user_logout, name='logout'),
    path('dashboard/', views.user_dashboard, name='dashboard'),
    path('profile/', views.users_profile, name='profile'),
    path('logout/', views.user_logout, name='logout'),

    # Pre-module-options-router
    path('pre_options/', views.user_options_pre, name='pre_options'),
    path('para_options/', views.user_options_para, name='para_options'),
    path('clinical_options/', views.user_options_clicnical, name='clinical_options'),
    
    
    path('app_data_repo_initialize/', views.data_repo, name='repo'),

]
