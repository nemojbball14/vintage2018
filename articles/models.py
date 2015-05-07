import os
from django.db import models


class Article(models.Model):
    """Holds the information for one Article"""

    title = models.CharField(max_length=50)
    intro = models.TextField()
    paragraph   = models.TextField()
    paragraph2  = models.TextField(blank=True)
    blockquote  = models.CharField(max_length=512)
    blockquote2 = models.CharField(max_length=512, blank=True)
    thumb_nail  = models.ImageField(upload_to=os.path.join('public', 'ArticlePictures'))

    article_slug = models.SlugField(unique=True)    

    def __unicode__(self):
        return self.title


class ArticlePicture(models.Model):
    """A picture that belongs to an Article."""
    article = models.ForeignKey(Article)
    caption = models.TextField(blank=True)
    pic = models.ImageField("Image", upload_to=os.path.join('public', 'ArticlePictures'))

    def __unicode__(self):
        return self.article.title+'-'+self.pic.name
