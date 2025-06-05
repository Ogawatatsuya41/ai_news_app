# news/admin.py

from django.contrib import admin
from .models import Article # 作成した Article モデルをインポート

@admin.register(Article) # Article モデルを管理サイトに登録するためのデコレータ
class ArticleAdmin(admin.ModelAdmin):
    # 管理サイトの一覧ページに表示するフィールドを指定
    list_display = ('title', 'source_name', 'published_at', 'created_at', 'updated_at')
    # 管理サイトで検索可能にするフィールドを指定
    search_fields = ('title', 'summary', 'url')
    # 管理サイトで絞り込み（フィルター）に使うフィールドを指定
    list_filter = ('source_name', 'published_at')
    # 編集画面で読み取り専用にするフィールドを指定
    readonly_fields = ('created_at', 'updated_at')
    # (任意) 編集画面のフィールドの表示順やグループ化を設定
    fieldsets = (
        (None, { # グループ名なし
            'fields': ('title', 'url', 'summary', 'source_name', 'published_at')
        }),
        ('システム情報', { # グループ名「システム情報」
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',) # デフォルトで折りたたんで表示
        }),
    )

# もし上記 @admin.register(Article) を使わない場合は、代わりに以下の1行を記述します。
# admin.site.register(Article, ArticleAdmin)
# もしくは、もっとシンプルに表示するだけなら admin.site.register(Article) でもOKです。