from django.shortcuts import render
from .models import Article

def article_list(request):
    # データベースから全記事を取得 (モデルのMetaクラスで設定した順序で)
    articles = Article.objects.all()

    # テンプレートに渡すデータ（コンテキスト）を辞書形式で作成
    context = {
        'articles': articles,
    }

    # テンプレートをレンダリングしてレスポンスを返す
    return render(request, 'news/article_list.html', context)