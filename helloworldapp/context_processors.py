from .models import Team

def user_teams(request):
    """
    ログインユーザーが所属しているチームをすべてのテンプレートで利用可能にする
    """
    if request.user.is_authenticated:
        teams = Team.objects.filter(members=request.user).prefetch_related('members')
        return {'user_teams': teams}
    return {'user_teams': []}
