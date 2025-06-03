from django import forms
from .models import Task, Project, User # Userモデルもインポート

class TaskForm(forms.ModelForm):
    # プロジェクトと担当者の選択肢を、未選択も許容するように調整
    project = forms.ModelChoiceField(
        queryset=Project.objects.all(),
        required=False, # プロジェクトは必須ではない
        label="プロジェクト",
        empty_label="----- (プロジェクトなし) -----" # 未選択時のラベル
    )
    assignee = forms.ModelChoiceField(
        queryset=User.objects.all(),
        required=False, # 担当者は必須ではない
        label="担当者",
        empty_label="----- (担当者なし) -----" # 未選択時のラベル
    )
    due_date = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date'}), # HTML5の日付選択ウィジェットを使用
        required=False, # 期限日も必須ではない
        label="期限日"
    )

    class Meta:
        model = Task
        fields = ['title', 'description', 'project', 'assignee', 'due_date', 'priority', 'status']
        # labels はMetaクラス内ではなく、フィールド定義時に直接指定する方が一般的です。
        # widgets も同様にフィールド定義時に指定できます。
        # もしフィールドごとに個別の設定が不要であれば、上記のように直接フィールド名をリストで指定するだけで十分です。

        # 以下のように widgets を使って、各フィールドのHTML属性などを細かく設定することも可能です。
        widgets = {
            'title': forms.TextInput(attrs={'placeholder': '例: 新しいウェブサイトのデザイン'}),
            'description': forms.Textarea(attrs={'rows': 4, 'placeholder': 'タスクの詳細な説明を入力します'}),
            # 'status': forms.Select(choices=Task.STATUS_CHOICES) # ModelFormは自動で設定してくれることが多い
        }
        # labels = {
        #     'title': 'タスク名',
        #     'description': '詳細説明',
        #     'priority': '優先度',
        #     'status': 'ステータス',
        # }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # フォームフィールドの表示名をモデルのverbose_nameから取得（もしモデルで定義されていれば）
        # もしくは、ここで動的にラベルを設定することも可能
        for field_name, field in self.fields.items():
            if not field.label: # 明示的にラベルが設定されていない場合
                field.label = Task._meta.get_field(field_name).verbose_name.capitalize()

        # projectとassigneeの選択肢に、現在のユーザーが選択しやすいような工夫も可能
        # 例えば、User.objects.filter(is_active=True) のようにアクティブユーザーのみに絞るなど