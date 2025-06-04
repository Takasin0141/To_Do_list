from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse #, Http404, HttpResponseForbidden
from .models import Task, Project
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import timedelta
from .forms import TaskForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.decorators import login_required
# from django.contrib import messages

# 4. メイン画面 (ダッシュボード) & タスク追加処理
# @login_required
def main_page(request):
    if request.method == 'POST' and 'title' in request.POST: # タスク追加フォームからのPOSTか判定（簡易的）
        form = TaskForm(request.POST)
        if form.is_valid():
            task_instance = form.save(commit=False)
            # if request.user.is_authenticated:
            #     task_instance.creator = request.user 
            task_instance.save()
            form.save_m2m()
            # messages.success(request, "新しいタスクが追加されました。")
            return redirect('helloworldapp:main_page')
    else:
        form = TaskForm() # GETリクエスト時や、タスク追加以外のPOSTの場合は空のフォーム

    tasks = Task.objects.all().order_by('due_date', 'priority')
    assigned_tasks_count = tasks.exclude(status='completed').count()
    due_soon_tasks = tasks.filter(
        due_date__gte=timezone.now().date(),
        due_date__lte=timezone.now().date() + timedelta(days=7),
        status__in=['pending', 'in_progress', 'on_hold']
    )
    due_soon_count = due_soon_tasks.count()
    completed_count = tasks.filter(status='completed').count()
    users = User.objects.all()
    projects_list = Project.objects.all()

    context = {
        'form': form, # タスク追加用フォーム
        'tasks': tasks,
        'assigned_tasks_count': assigned_tasks_count,
        'due_soon_count': due_soon_count,
        'completed_count': completed_count,
        'projects': projects_list,
        'users': users,
    }
    return render(request, 'helloworldapp/main_page.html', context)

# 1. ログイン画面
def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                next_url = request.GET.get('next')
                if next_url:
                    return redirect(next_url)
                return redirect('helloworldapp:main_page')
    else:
        form = AuthenticationForm()
    return render(request, 'helloworldapp/login.html', {'form': form, 'page_title': 'ログイン'})

# ログアウトビュー
def logout_view(request):
    logout(request)
    return redirect('helloworldapp:login_view')

# 2. 新規登録画面
def signup_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('helloworldapp:main_page')
    else:
        form = UserCreationForm()
    return render(request, 'helloworldapp/signup.html', {'form': form, 'page_title': '新規登録'})

# ★★★ タスク編集ビューを追加 ★★★
@login_required
def task_edit_view(request, task_id):
    task_instance = get_object_or_404(Task, id=task_id)
    
    # 権限チェックの例: タスクの担当者またはスーパーユーザーのみ編集可能
    # if task_instance.assignee != request.user and not request.user.is_superuser:
    #     # messages.error(request, "このタスクを編集する権限がありません。")
    #     return redirect('helloworldapp:task_detail_view', task_id=task_id)

    if request.method == 'POST':
        form = TaskForm(request.POST, instance=task_instance) # 既存インスタンスを指定
        if form.is_valid():
            form.save()
            # messages.success(request, f"タスク「{task_instance.title}」が更新されました。")
            return redirect('helloworldapp:task_detail_view', task_id=task_id)
    else:
        form = TaskForm(instance=task_instance) # 既存インスタンスのデータでフォームを初期化

    context = {
        'form': form,
        'task': task_instance, # テンプレートでタスク情報を参照できるように
        'page_title': f"タスク編集: {task_instance.title}"
    }
    return render(request, 'helloworldapp/task_edit.html', context) # 新しいテンプレートを指定

# 3. パスワード変更画面
def change_password_view(request):
    return HttpResponse("パスワード変更画面 (未実装)")

# 5. カレンダービュー
def calendar_view(request):
    return HttpResponse("カレンダービュー (未実装)")

# 6. マイタスクページ
@login_required
def my_tasks_view(request):
    user_tasks = Task.objects.filter(assignee=request.user).exclude(status='completed').order_by('due_date', 'priority')
    completed_user_tasks = Task.objects.filter(assignee=request.user, status='completed').order_by('-updated_at')
    context = {
        'user_tasks': user_tasks,
        'completed_user_tasks': completed_user_tasks,
        'page_title': 'マイタスク'
    }
    return render(request, 'helloworldapp/my_tasks.html', context)

# 7. チームダッシュボード
# @login_required
def team_dashboard_view(request):
    return HttpResponse("チームダッシュボード (未実装)")

# 8. プロジェクトボード
# @login_required
def project_board_view(request, project_id=None):
    return HttpResponse(f"プロジェクトボード (プロジェクトID: {project_id}) (未実装)")

# 9. タスク詳細ページ
@login_required
def task_detail_view(request, task_id):
    task = get_object_or_404(Task, id=task_id)
    context = {
        'task': task,
        'page_title': f"タスク詳細: {task.title}"
    }
    return render(request, 'helloworldapp/task_detail.html', context)

# 10. チームメンバー管理ページ
# @login_required
def team_member_management_view(request):
    return HttpResponse("チームメンバー管理ページ (未実装)")

# 11. アプリ設定ページ
# @login_required
def app_settings_view(request):
    return HttpResponse("アプリ設定ページ (未実装)")

# 12. マイページ (プロフィール設定など)
# @login_required
def my_page_view(request):
    return HttpResponse("マイページ (未実装)")

# 13. ヘルプ画面
def help_view(request):
    return HttpResponse("ヘルプ画面 (未実装)")