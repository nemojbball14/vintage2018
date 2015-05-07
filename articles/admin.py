from django.contrib import admin
from articles.models import Article, ArticlePicture


class ArticleAdmin(admin.ModelAdmin):
    prepopulated_fields = {"article_slug": ("title",)}
    list_display = ('title', 'article_slug')
    ordering = ('title',)


class ArticlePictureAdmin(admin.ModelAdmin):
    list_display = ('article', 'pic', 'caption')


admin.site.register(Article, ArticleAdmin)
admin.site.register(ArticlePicture, ArticlePictureAdmin)
