# news/models.py

from django.db import models
from django.utils import timezone

class Article(models.Model):
    title = models.CharField(verbose_name="タイトル", max_length=255)
    url = models.URLField(verbose_name="記事URL", unique=True, max_length=2000) # URLはユニーク（重複なし）に設定
    summary = models.TextField(verbose_name="概要", blank=True, null=True) # 概要は空でもOK
    published_at = models.DateTimeField(verbose_name="発行日時", blank=True, null=True) # 発行日時も空でもOK
    source_name = models.CharField(verbose_name="情報源", max_length=100, blank=True, null=True) # 情報源も空でもOK
    created_at = models.DateTimeField(verbose_name="登録日時", default=timezone.now) # このレコードが作成された日時（自動設定）
    updated_at = models.DateTimeField(verbose_name="更新日時", auto_now=True) # このレコードが更新された日時（自動更新）

    def __str__(self):
        # 管理画面などで記事がどのように表示されるかを定義 (記事タイトルを表示)
        return self.title

    class Meta:
        # 管理画面でのモデルの表示名を設定
        verbose_name = "ニュース記事"
        verbose_name_plural = "ニュース記事"
        # 記事のデフォルトの並び順を設定 (発行日時の新しい順、次に登録日時の新しい順)
        ordering = ['-published_at', '-created_at']