from django.contrib import admin
from .models import Project, Task

# Projectモデルを管理画面に登録
@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('name', 'created_at', 'updated_at') # 一覧画面に表示するフィールド
    search_fields = ('name', 'description') # 検索対象のフィールド
    list_filter = ('created_at',) # フィルタリングオプション

# Taskモデルを管理画面に登録
@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('title', 'project', 'assignee', 'due_date', 'status', 'priority', 'updated_at')
    search_fields = ('title', 'description')
    list_filter = ('status', 'priority', 'due_date', 'project', 'assignee')
    # 編集画面でのフィールドの順序やレイアウトもカスタマイズ可能です
    # fields = (...)
    # fieldsets = (...)

# もし上記のようなModelAdminクラスを使ったカスタマイズが不要で、
# 単純に登録するだけでよければ、以下のように記述することも可能です。
# admin.site.register(Project)
# admin.site.register(Task)