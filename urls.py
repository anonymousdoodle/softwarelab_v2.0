# flashlearn_app/urls.py
from django.urls import path
from . import views
from .views import delete_teacher

urlpatterns = [
    path('', views.home, name='home'),
    path('login/', views.login, name='login'),
    path('signup/', views.signup, name='signup'),
    path('manageadmins/', views.manageadmins, name='manageadmins'),
    path('manageusers/', views.manageusers, name='manageusers'),

    path('manageteachers/', views.manageteachers, name='manageteachers'),
    path('delete_teacher/<int:teacher_id>/', delete_teacher, name='delete_teacher'),

    path('editusers/<int:user_id>/', views.edit_user, name='edit_user'),
    path('editadmin/<int:admin_id>/', views.edit_admin, name='edit_admin'),
    path('update_user/<int:user_id>/', views.update_user, name='update_user'),
    path('update_admin/<int:user_id>/', views.update_admin, name='update_admin'),
    path('delete-user/<int:user_id>/', views.delete_user, name='delete_user'),
    path('delete-admin/<int:user_id>/', views.delete_admin, name='delete_admin'),

    path('add_teacher/', views.add_teacher, name='add_teacher'),
    #for editing teacher cards
    path('teachercards/<int:cardid>/', views.edit_tcards, name='edit_tcards'),
    path('update_tcards/<int:cardid>/', views.update_tcards, name='update_tcards'),


]
