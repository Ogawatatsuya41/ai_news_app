from django.shortcuts import render
from .models import Article
from django.core.paginator import Paginator
from django.db.models import Q # Qオブジェクトをインポート
from django.shortcuts import get_object_or_404
import pickle

def article_list(request):
    # まずは全記事を取得
    queryset = Article.objects.all()

    # URLから検索クエリを取得 (例: /news/?q=検索キーワード)
    query = request.GET.get('q')

    # もし検索クエリが存在すれば、それで記事を絞り込む
    if query:
        # Qオブジェクトを使って、タイトル(title)または概要(summary)に
        # クエリの文字列が含まれる(icontains)記事を検索する
        queryset = queryset.filter(
            Q(title__icontains=query) | Q(summary__icontains=query)
        )

    # Paginatorオブジェクトを作成。1ページに表示する記事の数を10件に設定
    paginator = Paginator(queryset, 10) # all_articles の代わりに queryset を使う

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # テンプレートに渡すデータに、検索クエリも追加する
    context = {
        'page_obj': page_obj,
        'query': query, # 検索キーワードをテンプレートに渡す
    }

    return render(request, 'news/article_list.html', context)

def article_detail(request, pk):
    article = get_object_or_404(Article, pk=pk)
    related_articles = []
    try:
        # 保存した類似度データを読み込む
        with open('similarity_matrix.pkl', 'rb') as f:
            similarity_data = pickle.load(f)

        all_pks = similarity_data['pks']
        matrix = similarity_data['matrix']

        # 現在の記事のインデックスを探す
        current_article_index = all_pks.index(pk)

        # 類似度スコアを取得し、(インデックス, スコア)のタプルのリストを作成
        similarity_scores = list(enumerate(matrix[current_article_index]))

        # 類似度が高い順にソート（自分自身は除く）
        sorted_scores = sorted(similarity_scores, key=lambda x: x[1], reverse=True)[1:6] # 自分を除き上位5件

        # 関連記事のpkを取得
        related_article_indices = [score[0] for score in sorted_scores]
        related_pks = [all_pks[i] for i in related_article_indices]

        # データベースから関連記事オブジェクトを取得
        related_articles = Article.objects.filter(pk__in=related_pks)

    except FileNotFoundError:
        # similarity_matrix.pkl がない場合は何もしない
        pass
    except ValueError:
        # 記事が類似度マトリックス計算後に作られた場合など
        pass

    context = {
        'article': article,
        'related_articles': related_articles, # 関連記事をコンテキストに追加
    }
    return render(request, 'news/article_detail.html', context)