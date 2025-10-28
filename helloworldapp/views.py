from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, HttpResponseForbidden, JsonResponse
from .models import Task, Project, Team 
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import timedelta
from .forms import TaskForm, TeamForm 
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.urls import reverse
from django.db.models import Count, Q

# (main_page や認証関連、タスクCRUD、チーム関連、その他既存のビューなどは変更なし)
# ... (既存のビュー関数のコード) ...

# 4. メイン画面 (ダッシュボード) & タスク追加処理
def main_page(request):
    if request.method == 'POST' and 'title' in request.POST and 'assignee' in request.POST : 
        form = TaskForm(request.POST)
        if form.is_valid():
            task_instance = form.save(commit=False)
            if request.user.is_authenticated:
                pass
            task_instance.save()
            form.save_m2m()
            messages.success(request, f"タスク「{task_instance.title}」が追加されました。")
            return redirect('helloworldapp:main_page')
    else:
        form = TaskForm()
    tasks = Task.objects.all().order_by('due_date', 'priority')
    # ログインユーザーの担当タスクのみをカウント
    if request.user.is_authenticated:
        assigned_tasks_count = Task.objects.filter(assignee=request.user).exclude(status='completed').count()
    else:
        assigned_tasks_count = 0
    # ログインユーザーの期限間近タスクのみをカウント
    if request.user.is_authenticated:
        due_soon_tasks = Task.objects.filter(
            assignee=request.user,
            due_date__gte=timezone.now().date(),
            due_date__lte=timezone.now().date() + timedelta(days=7),
            status__in=['pending', 'in_progress', 'on_hold']
        )
        due_soon_count = due_soon_tasks.count()
        completed_count = Task.objects.filter(assignee=request.user, status='completed').count()
    else:
        due_soon_count = 0
        completed_count = 0
    users = User.objects.all()
    projects_list = Project.objects.all()
    context = {
        'form': form, 'tasks': tasks, 'assigned_tasks_count': assigned_tasks_count,
        'due_soon_count': due_soon_count, 'completed_count': completed_count,
        'projects': projects_list, 'users': users,
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
                messages.info(request, f"ようこそ、{username} さん！")
                next_url = request.GET.get('next')
                if next_url: return redirect(next_url)
                return redirect('helloworldapp:main_page')
            else: messages.error(request,"ユーザー名またはパスワードが無効です。")
        else: messages.error(request,"入力内容に誤りがあります。")
    else: form = AuthenticationForm()
    return render(request, 'helloworldapp/login.html', {'form': form, 'page_title': 'ログイン'})

# ログアウトビュー
def logout_view(request):
    logout(request)
    messages.info(request, "ログアウトしました。")
    return redirect('helloworldapp:login_view')

# 2. 新規登録画面
def signup_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "登録が完了しました。ようこそ！")
            return redirect('helloworldapp:main_page')
        else: messages.error(request, "登録に失敗しました。入力内容を確認してください。")
    else: form = UserCreationForm()
    return render(request, 'helloworldapp/signup.html', {'form': form, 'page_title': '新規登録'})

# チーム作成ビュー
@login_required
def team_create_view(request):
    if request.method == 'POST':
        form = TeamForm(request.POST)
        if form.is_valid():
            team = form.save(commit=False)
            team.created_by = request.user
            team.save()
            team.members.add(request.user)
            messages.success(request, f"チーム「{team.name}」が作成されました。")
            return redirect('helloworldapp:team_list_view')
        else: messages.error(request, "チームの作成に失敗しました。入力内容を確認してください。")
    else: form = TeamForm()
    context = {'form': form, 'page_title': '新しいチームを作成'}
    return render(request, 'helloworldapp/team_create_form.html', context)

# チーム一覧ビュー
@login_required
def team_list_view(request):
    teams = request.user.member_of_teams.all().prefetch_related('members', 'created_by').order_by('name')
    context = {'teams': teams, 'page_title': '参加中のチーム一覧'}
    return render(request, 'helloworldapp/team_list.html', context)

# チーム詳細ビュー
@login_required
def team_detail_view(request, team_id):
    team = get_object_or_404(Team.objects.prefetch_related('members', 'created_by'), id=team_id)
    if not request.user.is_superuser and request.user not in team.members.all():
        messages.error(request, "このチームの詳細を閲覧する権限がありません。")
        return redirect('helloworldapp:team_list_view')
    context = {'team': team, 'members': team.members.all(), 'page_title': f"チーム詳細: {team.name}"}
    return render(request, 'helloworldapp/team_detail.html', context)

# チームメンバー管理ビュー
@login_required
def team_member_management_view(request, team_id):
    team = get_object_or_404(Team.objects.prefetch_related('members', 'created_by'), id=team_id)
    if not (request.user == team.created_by or request.user.is_superuser):
        messages.error(request, "チームメンバーを管理する権限がありません。")
        return redirect('helloworldapp:team_detail_view', team_id=team.id)
    if request.method == 'POST':
        if 'add_member' in request.POST:
            user_id_to_add = request.POST.get('user_to_add')
            if user_id_to_add:
                try:
                    user_to_add = User.objects.get(id=user_id_to_add)
                    if user_to_add not in team.members.all(): team.members.add(user_to_add); messages.success(request, f"ユーザー「{user_to_add.username}」をチーム「{team.name}」に追加しました。")
                    else: messages.warning(request, f"ユーザー「{user_to_add.username}」は既にチーム「{team.name}」のメンバーです。")
                except User.DoesNotExist: messages.error(request, "指定されたユーザーが見つかりません。")
            else: messages.error(request, "追加するユーザーを選択してください。")
        elif 'remove_member' in request.POST:
            user_id_to_remove = request.POST.get('user_to_remove')
            if user_id_to_remove:
                try:
                    user_to_remove = User.objects.get(id=user_id_to_remove)
                    if user_to_remove in team.members.all():
                        if user_to_remove == team.created_by and team.members.count() == 1 : messages.error(request, f"チーム作成者であり最後のメンバーである「{user_to_remove.username}」を削除することはできません。")
                        elif user_to_remove == team.created_by: messages.warning(request, f"チーム作成者「{user_to_remove.username}」の削除は、現在この画面からは行えません。")
                        else: team.members.remove(user_to_remove); messages.success(request, f"ユーザー「{user_to_remove.username}」をチーム「{team.name}」から削除しました。")
                    else: messages.warning(request, f"ユーザー「{user_to_remove.username}」はチーム「{team.name}」のメンバーではありません。")
                except User.DoesNotExist: messages.error(request, "指定されたユーザーが見つかりません。")
            else: messages.error(request, "削除するユーザーを指定してください。")
        return redirect('helloworldapp:manage_team_members_view', team_id=team.id)
    current_members = team.members.all().order_by('username')
    potential_new_members = User.objects.exclude(member_of_teams=team).order_by('username')
    context = {'team': team, 'current_members': current_members, 'potential_new_members': potential_new_members, 'page_title': f"「{team.name}」メンバー管理"}
    return render(request, 'helloworldapp/manage_team_members.html', context)

# チーム編集ビュー
@login_required
def team_edit_view(request, team_id):
    team_instance = get_object_or_404(Team, id=team_id)
    if not (request.user == team_instance.created_by or request.user.is_superuser):
        messages.error(request, "チーム情報を編集する権限がありません。")
        return redirect('helloworldapp:team_detail_view', team_id=team_instance.id)
    if request.method == 'POST':
        form = TeamForm(request.POST, instance=team_instance)
        if form.is_valid():
            form.save(); messages.success(request, f"チーム「{team_instance.name}」の情報が更新されました。")
            return redirect('helloworldapp:team_detail_view', team_id=team_instance.id)
        else: messages.error(request, "チーム情報の更新に失敗しました。入力内容を確認してください。")
    else: form = TeamForm(instance=team_instance)
    context = {'form': form, 'team': team_instance, 'page_title': f"チーム編集: {team_instance.name}"}
    return render(request, 'helloworldapp/team_edit_form.html', context)

# チーム削除ビュー
@login_required
def team_delete_view(request, team_id):
    team_instance = get_object_or_404(Team, id=team_id)
    if not (request.user == team_instance.created_by or request.user.is_superuser):
        messages.error(request, "チームを削除する権限がありません。")
        return redirect('helloworldapp:team_detail_view', team_id=team_instance.id)
    if request.method == 'POST':
        team_name = team_instance.name; team_instance.delete()
        messages.success(request, f"チーム「{team_name}」を削除しました。")
        return redirect('helloworldapp:team_list_view')
    context = {'team': team_instance, 'page_title': f"チーム削除確認: {team_instance.name}"}
    return render(request, 'helloworldapp/team_confirm_delete.html', context)

# チーム脱退ビュー
@login_required
def leave_team_view(request, team_id):
    team = get_object_or_404(Team, id=team_id)
    current_user = request.user
    if current_user not in team.members.all():
        messages.error(request, f"あなたはチーム「{team.name}」のメンバーではありません。")
        return redirect('helloworldapp:team_detail_view', team_id=team.id)
    if current_user == team.created_by:
        if team.members.count() == 1:
            messages.error(request, "あなたがこのチームの最後のメンバー（かつ作成者）であるため、脱退できません。チームを削除するか、他のメンバーを追加してください。")
            return redirect('helloworldapp:team_detail_view', team_id=team.id)
    if request.method == 'POST':
        team.members.remove(current_user)
        messages.success(request, f"チーム「{team.name}」から脱退しました。")
        return redirect('helloworldapp:team_list_view')
    context = {'team': team, 'page_title': f"チーム「{team.name}」から脱退しますか？"}
    return render(request, 'helloworldapp/team_confirm_leave.html', context)

# チームダッシュボードビュー
@login_required
def team_dashboard_view(request, team_id):
    team = get_object_or_404(Team.objects.prefetch_related('members'), id=team_id)
    if not request.user.is_superuser and request.user not in team.members.all():
        messages.error(request, "このチームダッシュボードを閲覧する権限がありません。")
        return redirect('helloworldapp:team_list_view') 
    team_tasks = team.team_tasks.all().order_by('status', 'priority', 'due_date')
    status_choices = Task.STATUS_CHOICES
    tasks_by_status_dict = {status_value: [] for status_value, _ in status_choices}
    for task in team_tasks:
        if task.status in tasks_by_status_dict: tasks_by_status_dict[task.status].append(task)
    board_columns = []
    for status_value, status_display in status_choices:
        board_columns.append({'id': status_value, 'name': status_display, 'tasks': tasks_by_status_dict.get(status_value, [])})
    context = {'team': team, 'board_columns': board_columns, 'page_title': f"チームダッシュボード: {team.name}"}
    return render(request, 'helloworldapp/team_dashboard.html', context)

# タスク関連ビュー (変更なし)
# ... (task_edit_view, task_delete_view) ...
@login_required
def task_edit_view(request, task_id):
    task_instance = get_object_or_404(Task, id=task_id)
    if request.method == 'POST':
        form = TaskForm(request.POST, instance=task_instance)
        if form.is_valid():
            form.save()
            messages.success(request, f"タスク「{task_instance.title}」が更新されました。")
            return redirect('helloworldapp:task_detail_view', task_id=task_id)
        else: messages.error(request, "タスクの更新に失敗しました。入力内容を確認してください。")
    else: form = TaskForm(instance=task_instance)
    context = {'form': form, 'task': task_instance, 'page_title': f"タスク編集: {task_instance.title}"}
    return render(request, 'helloworldapp/task_edit.html', context)

@login_required
def task_delete_view(request, task_id):
    task_instance = get_object_or_404(Task, id=task_id)
    if request.method == 'POST':
        task_title = task_instance.title; task_instance.delete()
        messages.success(request, f"タスク「{task_title}」を削除しました。")
        return redirect('helloworldapp:main_page')
    context = {'task': task_instance, 'page_title': f"タスク削除確認: {task_instance.title}"}
    return render(request, 'helloworldapp/task_confirm_delete.html', context)

# カレンダービュー (変更なし)
@login_required
def calendar_view(request):
    user_tasks = Task.objects.filter(assignee=request.user, due_date__isnull=False).select_related('project')
    events_data = []
    for task in user_tasks:
        event_color = '';
        if task.status == 'completed': event_color = 'grey'
        elif task.due_date < timezone.now().date() and task.status != 'completed': event_color = 'red'
        events_data.append({
            'id': task.id, 'title': task.title, 'start': task.due_date.isoformat(),
            'url': reverse('helloworldapp:task_detail_view', args=[task.id]), 'allDay': True,
            'color': event_color if event_color else None, 'borderColor': event_color if event_color else None,
        })
    context = {'events_list': events_data, 'page_title': 'カレンダービュー'}
    return render(request, 'helloworldapp/calendar.html', context)

# マイタスクページ
@login_required
def my_tasks_view(request):
    if request.method == 'POST':
        # タスク追加処理
        form = TaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.assignee = request.user
            task.save()
            form.save_m2m()
            messages.success(request, f"タスク「{task.title}」が追加されました。")
            return redirect('helloworldapp:my_tasks_view')
        else:
            messages.error(request, "タスクの追加に失敗しました。入力内容を確認してください。")
    else:
        form = TaskForm()
    
    user_tasks = Task.objects.filter(assignee=request.user).exclude(status='completed').order_by('due_date', 'priority')
    completed_user_tasks = Task.objects.filter(assignee=request.user, status='completed').order_by('-updated_at')
    projects = Project.objects.all()
    
    context = {
        'user_tasks': user_tasks, 
        'completed_user_tasks': completed_user_tasks, 
        'projects': projects,
        'form': form,
        'page_title': 'マイタスク'
    }
    return render(request, 'helloworldapp/my_tasks.html', context)

# プロジェクトボードビュー (変更なし)
@login_required
def project_board_view(request, project_id):
    project = get_object_or_404(Project, id=project_id)
    project_tasks = Task.objects.filter(project=project).order_by('priority', 'due_date')
    status_choices = Task.STATUS_CHOICES 
    tasks_by_status_dict = {status_value: [] for status_value, _ in status_choices}
    for task in project_tasks:
        if task.status in tasks_by_status_dict: tasks_by_status_dict[task.status].append(task)
    board_columns = []
    for status_value, status_display in status_choices:
        board_columns.append({'id': status_value, 'name': status_display, 'tasks': tasks_by_status_dict.get(status_value, [])})
    context = {'project': project, 'board_columns': board_columns, 'page_title': f"プロジェクトボード: {project.name}"}
    return render(request, 'helloworldapp/project_board.html', context)

# タスク詳細ページ (変更なし)
@login_required
def task_detail_view(request, task_id):
    task = get_object_or_404(Task, id=task_id)
    context = {'task': task, 'page_title': f"タスク詳細: {task.title}"}
    return render(request, 'helloworldapp/task_detail.html', context)

# マイページビュー (変更なし)
@login_required
def my_page_view(request):
    current_user = request.user
    assigned_tasks = Task.objects.filter(assignee=current_user)
    total_assigned_tasks = assigned_tasks.count()
    completed_assigned_tasks = assigned_tasks.filter(status='completed').count()
    active_assigned_tasks = total_assigned_tasks - completed_assigned_tasks
    context = {
        'current_user': current_user, 'total_assigned_tasks': total_assigned_tasks,
        'completed_assigned_tasks': completed_assigned_tasks, 'active_assigned_tasks': active_assigned_tasks,
        'page_title': 'マイページ'
    }
    return render(request, 'helloworldapp/my_page.html', context)

# プロジェクト一覧ビュー
@login_required
def project_list_view(request):
    projects = Project.objects.all().order_by('-created_at')
    context = {'projects': projects, 'page_title': 'プロジェクト一覧'}
    return render(request, 'helloworldapp/project_list.html', context)

# プロジェクト作成ビュー
@login_required
def project_create_view(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        description = request.POST.get('description', '')
        if name:
            project = Project.objects.create(name=name, description=description)
            messages.success(request, f"プロジェクト「{project.name}」が作成されました。")
            return redirect('helloworldapp:project_list_view')
        else:
            messages.error(request, "プロジェクト名を入力してください。")
    context = {'page_title': '新しいプロジェクトを作成'}
    return render(request, 'helloworldapp/project_create.html', context)

# プロジェクト詳細ビュー
@login_required
def project_detail_view(request, project_id):
    project = get_object_or_404(Project, id=project_id)
    project_tasks = Task.objects.filter(project=project).order_by('-created_at')
    context = {'project': project, 'project_tasks': project_tasks, 'page_title': f"プロジェクト詳細: {project.name}"}
    return render(request, 'helloworldapp/project_detail.html', context)

# プロジェクト編集ビュー
@login_required
def project_edit_view(request, project_id):
    project = get_object_or_404(Project, id=project_id)
    if request.method == 'POST':
        name = request.POST.get('name')
        description = request.POST.get('description', '')
        if name:
            project.name = name
            project.description = description
            project.save()
            messages.success(request, f"プロジェクト「{project.name}」が更新されました。")
            return redirect('helloworldapp:project_detail_view', project_id=project.id)
        else:
            messages.error(request, "プロジェクト名を入力してください。")
    context = {'project': project, 'page_title': f"プロジェクト編集: {project.name}"}
    return render(request, 'helloworldapp/project_edit.html', context)

# プロジェクト削除ビュー
@login_required
def project_delete_view(request, project_id):
    project = get_object_or_404(Project, id=project_id)
    if request.method == 'POST':
        project_name = project.name
        project.delete()
        messages.success(request, f"プロジェクト「{project_name}」を削除しました。")
        return redirect('helloworldapp:project_list_view')
    context = {'project': project, 'page_title': f"プロジェクト削除確認: {project.name}"}
    return render(request, 'helloworldapp/project_confirm_delete.html', context)

# 11. アプリ設定ページ
@login_required # ★★★ ログイン必須とする ★★★
def app_settings_view(request): # ★★★ プレースホルダーから修正 ★★★
    context = {
        'page_title': 'アプリ設定'
    }
    return render(request, 'helloworldapp/app_settings.html', context) # 新しいテンプレートを指定

# レポートビュー
@login_required
def report_view(request):
    # タスク統計
    total_tasks = Task.objects.count()
    completed_tasks = Task.objects.filter(status='completed').count()
    pending_tasks = Task.objects.filter(status='pending').count()
    in_progress_tasks = Task.objects.filter(status='in_progress').count()
    
    # プロジェクト統計
    total_projects = Project.objects.count()
    
    # チーム統計
    total_teams = Team.objects.count()
    
    # ユーザー統計
    total_users = User.objects.count()
    
    # 最近の活動（過去30日）
    thirty_days_ago = timezone.now() - timedelta(days=30)
    recent_tasks = Task.objects.filter(created_at__gte=thirty_days_ago).count()
    recent_projects = Project.objects.filter(created_at__gte=thirty_days_ago).count()
    
    # 完了率
    completion_rate = (completed_tasks / total_tasks * 100) if total_tasks > 0 else 0
    
    # 期限間近のタスク
    due_soon_tasks = Task.objects.filter(
        due_date__gte=timezone.now().date(),
        due_date__lte=timezone.now().date() + timedelta(days=7),
        status__in=['pending', 'in_progress']
    ).count()
    
    context = {
        'page_title': 'レポート',
        'total_tasks': total_tasks,
        'completed_tasks': completed_tasks,
        'pending_tasks': pending_tasks,
        'in_progress_tasks': in_progress_tasks,
        'total_projects': total_projects,
        'total_teams': total_teams,
        'total_users': total_users,
        'recent_tasks': recent_tasks,
        'recent_projects': recent_projects,
        'completion_rate': round(completion_rate, 1),
        'due_soon_tasks': due_soon_tasks,
    }
    return render(request, 'helloworldapp/report.html', context)

# タスクステータス更新API
@login_required
def update_task_status(request, task_id):
    if request.method == 'POST':
        try:
            import json
            data = json.loads(request.body)
            new_status = data.get('status')
            
            task = get_object_or_404(Task, id=task_id)
            
            # 権限チェック（タスクの担当者またはスーパーユーザーのみ）
            if not (request.user == task.assignee or request.user.is_superuser):
                return JsonResponse({'success': False, 'error': '権限がありません'}, status=403)
            
            # ステータスを更新
            task.status = new_status
            task.save()
            
            return JsonResponse({'success': True, 'message': 'ステータスが更新されました'})
            
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)}, status=500)
    
    return JsonResponse({'success': False, 'error': '無効なリクエストです'}, status=400)

# 13. ヘルプ画面
def help_view(request):
    context = {
        'page_title': 'ヘルプ／使い方'
    }
    return render(request, 'helloworldapp/help.html', context)