from django.contrib import admin
from .models import Project, Task, Team # ★★★ Teamモデルをインポート ★★★

@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('name', 'created_at', 'updated_at')
    search_fields = ('name', 'description')
    list_filter = ('created_at',)

@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('title', 'project', 'assignee', 'due_date', 'status', 'priority', 'updated_at')
    search_fields = ('title', 'description')
    list_filter = ('status', 'priority', 'due_date', 'project', 'assignee')

# ★★★ Teamモデルを管理画面に登録 ★★★
@admin.register(Team)
class TeamAdmin(admin.ModelAdmin):
    list_display = ('name', 'created_by', 'created_at', 'get_member_count') # 一覧画面に表示するフィールド
    search_fields = ('name', 'description') # 検索対象のフィールド
    list_filter = ('created_at',) # フィルタリングオプション
    filter_horizontal = ('members',) # ManyToManyField のウィジェットを使いやすくする

    def get_member_count(self, obj):
        return obj.members.count()
    get_member_count.short_description = 'メンバー数' # カラムのヘッダー名