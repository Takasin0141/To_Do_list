from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class Project(models.Model):
    name = models.CharField(max_length=100, verbose_name="プロジェクト名")
    description = models.TextField(blank=True, null=True, verbose_name="説明")
    created_at = models.DateTimeField(default=timezone.now, verbose_name="作成日時")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="更新日時")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "プロジェクト"
        verbose_name_plural = "プロジェクト"

class Team(models.Model): # TeamモデルがTaskモデルより先に定義されていることを確認
    name = models.CharField(max_length=100, unique=True, verbose_name="チーム名")
    description = models.TextField(blank=True, null=True, verbose_name="チームの説明")
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name="created_teams", verbose_name="作成者")
    members = models.ManyToManyField(User, related_name="member_of_teams", verbose_name="メンバー")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="作成日時")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="更新日時")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "チーム"
        verbose_name_plural = "チーム"
        ordering = ['name']

class Task(models.Model):
    STATUS_CHOICES = [
        ('pending', '未着手'),
        ('in_progress', '進行中'),
        ('completed', '完了'),
        ('on_hold', '保留'),
    ]

    PRIORITY_CHOICES = [
        (1, '低'),
        (2, '中'),
        (3, '高'),
    ]

    title = models.CharField(max_length=200, verbose_name="タスク名")
    description = models.TextField(blank=True, null=True, verbose_name="詳細説明")
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name="tasks", blank=True, null=True, verbose_name="プロジェクト")
    assignee = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True, related_name="assigned_tasks", verbose_name="担当者")
    
    # ★★★ assigned_team フィールドを追加 ★★★
    assigned_team = models.ForeignKey(
        Team, 
        on_delete=models.SET_NULL, # チームが削除されてもタスクは残り、チーム割り当てがNULLになる
        null=True, 
        blank=True, # チーム割り当ては任意
        related_name="team_tasks", # Teamオブジェクトから .team_tasks.all() でタスクを取得可能
        verbose_name="担当チーム"
    )
    
    due_date = models.DateField(blank=True, null=True, verbose_name="期限日")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending', verbose_name="ステータス")
    priority = models.IntegerField(choices=PRIORITY_CHOICES, default=2, verbose_name="優先度")
    created_at = models.DateTimeField(default=timezone.now, verbose_name="作成日時")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="更新日時")

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "タスク"
        verbose_name_plural = "タスク"
        ordering = ['-created_at']