from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

app_name = 'helloworldapp'

urlpatterns = [
    path('', views.main_page, name='main_page'),
    path('login/', views.login_view, name='login_view'),
    path('logout/', views.logout_view, name='logout_view'),
    path('signup/', views.signup_view, name='signup_view'),
    path('my_tasks/', views.my_tasks_view, name='my_tasks_view'),
    path('task/<int:task_id>/', views.task_detail_view, name='task_detail_view'),
    path('task/<int:task_id>/edit/', views.task_edit_view, name='task_edit_view'),
    path('task/<int:task_id>/delete/', views.task_delete_view, name='task_delete_view'),
    
    path('password_change/', 
         auth_views.PasswordChangeView.as_view(
             template_name='helloworldapp/password_change_form.html',
             success_url='/todo/password_change/done/' 
         ), 
         name='password_change'),
    path('password_change/done/', 
         auth_views.PasswordChangeDoneView.as_view(
             template_name='helloworldapp/password_change_done.html'
         ), 
         name='password_change_done'),

    path('project/<int:project_id>/board/', views.project_board_view, name='project_board_view'),
    path('my_page/', views.my_page_view, name='my_page_view'),
    path('calendar/', views.calendar_view, name='calendar_view'),
    path('teams/create/', views.team_create_view, name='team_create_view'),
    path('teams/', views.team_list_view, name='team_list_view'),
    path('teams/<int:team_id>/', views.team_detail_view, name='team_detail_view'),
    path('teams/<int:team_id>/manage_members/', views.team_member_management_view, name='manage_team_members_view'),
    path('teams/<int:team_id>/edit/', views.team_edit_view, name='team_edit_view'),
    path('teams/<int:team_id>/delete/', views.team_delete_view, name='team_delete_view'),
    path('teams/<int:team_id>/leave/', views.leave_team_view, name='leave_team_view'),
    path('teams/<int:team_id>/dashboard/', views.team_dashboard_view, name='team_dashboard_view'),
    path('help/', views.help_view, name='help_view'),
    path('settings/', views.app_settings_view, name='app_settings_view'), # ★★★ アプリ設定ビューへのパスを追加 ★★★
]