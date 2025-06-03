from django.contrib import admin
from django.urls import path, include # include をインポート

urlpatterns = [
    path('admin/', admin.site.urls),
    path('todo/', include('helloworldapp.urls')), # helloworldappのurls.pyを読み込む
    # 他のアプリケーションのURLをここに追加することもできます
]