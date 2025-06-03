from django.db import models
from django.contrib.auth.models import User # Djangoの組み込みUserモデルを利用
from django.utils import timezone

class Project(models.Model):
    name = models.CharField(max_length=100, verbose_name="プロジェクト名")
    description = models.TextField(blank=True, null=True, verbose_name="説明")
    # owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="owned_projects", verbose_name="オーナー") # 必要に応じて
    created_at = models.DateTimeField(default=timezone.now, verbose_name="作成日時")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="更新日時")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "プロジェクト"
        verbose_name_plural = "プロジェクト"

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
    due_date = models.DateField(blank=True, null=True, verbose_name="期限日")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending', verbose_name="ステータス")
    priority = models.IntegerField(choices=PRIORITY_CHOICES, default=2, verbose_name="優先度")
    created_at = models.DateTimeField(default=timezone.now, verbose_name="作成日時")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="更新日時")
    # completed_at = models.DateTimeField(blank=True, null=True, verbose_name="完了日時") # 必要に応じて

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "タスク"
        verbose_name_plural = "タスク"
        ordering = ['-created_at'] # 作成日時の降順で並べるのが一般的

# 今後、チーム、通知などのモデルもここに追加していくことができます。
# class Team(models.Model):
#     name = models.CharField(max_length=100)
#     members = models.ManyToManyField(User, related_name="teams")
#     # ...