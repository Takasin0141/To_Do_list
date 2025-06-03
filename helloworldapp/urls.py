from django.urls import path
from . import views

app_name = 'helloworldapp'  # アプリケーションの名前空間

urlpatterns = [
    path('', views.main_page, name='main_page'),
    path('login/', views.login_view, name='login_view'),
    path('logout/', views.logout_view, name='logout_view'),
    path('signup/', views.signup_view, name='signup_view'),
    path('my_tasks/', views.my_tasks_view, name='my_tasks_view'),
    path('task/<int:task_id>/', views.task_detail_view, name='task_detail_view'), # ★★★ タスク詳細ビューへのパスを追加 ★★★
    
    # 今後実装するビューのためのURLパターンのプレースホルダー
    # path('password_change/', views.change_password_view, name='change_password_view'),
    # path('calendar/', views.calendar_view, name='calendar_view'),
    # path('team_dashboard/', views.team_dashboard_view, name='team_dashboard_view'),
    # path('project/<int:project_id>/', views.project_board_view, name='project_board_view'),
    # path('team_management/', views.team_member_management_view, name='team_member_management_view'),
    # path('settings/', views.app_settings_view, name='app_settings_view'),
    # path('my_page/', views.my_page_view, name='my_page_view'),
    # path('help/', views.help_view, name='help_view'),
]