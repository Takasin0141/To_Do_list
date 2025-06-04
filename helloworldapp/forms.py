from django import forms
from .models import Task, Project, User, Team # Teamモデルをインポート

class TaskForm(forms.ModelForm):
    project = forms.ModelChoiceField(
        queryset=Project.objects.all(),
        required=False,
        label="プロジェクト",
        empty_label="----- (プロジェクトなし) -----"
    )
    assignee = forms.ModelChoiceField(
        queryset=User.objects.all().order_by('username'), # ユーザー名順で表示
        required=False,
        label="担当者",
        empty_label="----- (担当者なし) -----"
    )
    assigned_team = forms.ModelChoiceField(
        queryset=Team.objects.all().order_by('name'), # チーム名順で表示
        required=False, # チーム割り当ては必須ではない
        label="担当チーム",
        empty_label="----- (チームなし) -----" # 未選択時のラベル
    )
    due_date = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date'}),
        required=False,
        label="期限日"
    )

    class Meta:
        model = Task
        fields = [
            'title', 
            'description', 
            'project', 
            'assignee', 
            'assigned_team', 
            'due_date', 
            'priority', 
            'status'
        ]
        widgets = {
            'title': forms.TextInput(attrs={'placeholder': '例: 新しいウェブサイトのデザイン'}),
            'description': forms.Textarea(attrs={'rows': 4, 'placeholder': 'タスクの詳細な説明を入力します'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if hasattr(Task._meta.get_field(field_name), 'verbose_name'):
                 model_field_verbose_name = Task._meta.get_field(field_name).verbose_name
                 if model_field_verbose_name and not field.label:
                    field.label = model_field_verbose_name.capitalize()

class TeamForm(forms.ModelForm): # ★★★ この TeamForm クラスが重要です ★★★
    class Meta:
        model = Team # Teamモデルを参照
        fields = ['name', 'description'] # ユーザーに入力してもらうフィールド
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': '例: 開発チームA、マーケティング部門'}),
            'description': forms.Textarea(attrs={'rows': 3, 'placeholder': 'チームの目的や概要などを入力します'}),
        }
        labels = { 
            'name': 'チーム名',
            'description': 'チームの説明',
        }
        help_texts = { 
            'name': '他のチームと区別できる一意のチーム名を入力してください。',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['name'].required = True # チーム名は必須