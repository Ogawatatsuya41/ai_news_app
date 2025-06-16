import pickle
from django.core.management.base import BaseCommand
from news.models import Article
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

class Command(BaseCommand):
    help = 'Builds and saves the article similarity matrix'

    def handle(self, *args, **options):
        self.stdout.write("Fetching articles...")
        # タイトルが空でない記事のみを対象
        articles = list(Article.objects.exclude(title__exact='').order_by('pk'))
        if not articles:
            self.stderr.write("No articles found.")
            return

        # 各記事のタイトルをリストに格納
        titles = [article.title for article in articles]

        self.stdout.write("Building TF-IDF matrix...")
        # TfidfVectorizerを初期化（日本語なので、単語の分割は簡易的）
        vectorizer = TfidfVectorizer(analyzer='char', ngram_range=(2, 4))
        tfidf_matrix = vectorizer.fit_transform(titles)

        self.stdout.write("Calculating cosine similarity...")
        # コサイン類似度を計算
        similarity_matrix = cosine_similarity(tfidf_matrix)

        # 計算結果をファイルに保存
        data_to_save = {
            'pks': [article.pk for article in articles],
            'matrix': similarity_matrix,
        }
        with open('similarity_matrix.pkl', 'wb') as f:
            pickle.dump(data_to_save, f)

        self.stdout.write(self.style.SUCCESS("Successfully built and saved similarity matrix to similarity_matrix.pkl"))