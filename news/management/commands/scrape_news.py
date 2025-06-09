# news/management/commands/scrape_news.py

import time
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from datetime import datetime
#from dateutil.parser import parse
from django.core.management.base import BaseCommand
from django.utils import timezone
from news.models import Article

class Command(BaseCommand):
    help = 'Scrapes news articles from ITmedia AI+ archive page'

    def handle(self, *args, **options):
        # ★ 対象URLがアーカイブページに変わっているため、URLを変更します。
        # 実際にはトップページと同じ内容ですが、構造が分かりやすいこちらのURLを元にします。
        TARGET_URL = 'https://www.itmedia.co.jp/aiplus/subtop/archive/2506.html'
        self.stdout.write(self.style.SUCCESS(f'Scraping started from: {TARGET_URL}'))

        try:
            response = requests.get(TARGET_URL)
            response.raise_for_status()
        except requests.RequestException as e:
            self.stderr.write(self.style.ERROR(f'Error fetching URL: {e}'))
            return

        soup = BeautifulSoup(response.content, 'html.parser')
        
        # ★★ 新しいHTML構造に合わせたCSSセレクタに変更 ★★
        # 「記事一覧」の箱の中にある、各記事の<li>タグを全て取得します。
        article_elements = soup.select('div.colBoxBacknumber div.colBoxUlist li')
        
        # (デバッグ用) 記事がいくつ見つかったか表示
        self.stdout.write(f"DEBUG: Found {len(article_elements)} article elements.")

        if not article_elements:
            self.stdout.write(self.style.WARNING('No articles found. The CSS selector might be outdated.'))
            return

        saved_count = 0
        skipped_count = 0

        # 取得した各<li>要素をループ処理
        for elem in article_elements:
            try:
                # <li>の中から<a>タグ（タイトルとURLを持つ）を探す
                title_elem = elem.select_one('a')
                if not title_elem:
                    continue
                
                # タイトルとURLを取得
                title = title_elem.get_text(strip=True)
                relative_url = title_elem['href']
                absolute_url = urljoin(TARGET_URL, relative_url)

                # 既に同じURLの記事が存在しないかチェック
                if Article.objects.filter(url=absolute_url).exists():
                    skipped_count += 1
                    continue

                # ★ 概要（サマリー）の取得処理は削除 ★
                # このページには概要がないため、summaryは空のままDBに保存されます。
                # （モデル定義で blank=True, null=True としているので問題ありません）

                # <li>の中から発行日時の<span>タグを探す
                time_elem = elem.select_one('span.colBoxUlistDate')
                published_str = time_elem.get_text(strip=True) if time_elem else ""
                
                published_at = None
                if published_str:
                    # "(2025年6月7日)" のような文字列からカッコを削除
                    clean_published_str = published_str.strip('（）')
                    parsed_time = datetime.strptime(clean_published_str, "%Y年%m月%d日")
                    published_at = timezone.make_aware(parsed_time)

                # データベースに保存
                Article.objects.create(
                    title=title,
                    url=absolute_url,
                    published_at=published_at,
                    source_name="ITmedia NEWS AI+"
                )
                saved_count += 1
                self.stdout.write(self.style.SUCCESS(f'Saved: {title}'))

            except Exception as e:
                self.stderr.write(self.style.ERROR(f'Error processing an article "{title[:20]}...": {e}'))
            
            time.sleep(1)

        self.stdout.write(self.style.SUCCESS(f'Scraping finished. Saved {saved_count} new articles. Skipped {skipped_count} existing articles.'))