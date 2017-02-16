import datetime

from django.db import models
from django.template.defaultfilters import slugify
from django.conf import settings
from django.db.models import permalink

from tags.models import Tag
from categories.models import Category


class Post(models.Model):
    title = models.CharField(max_length=255)
    slug = models.SlugField(max_length=256, default="")    
    url = models.URLField(default="", null=True, blank=True)
    body = models.TextField(default="", null=True, blank=True)

    pub_date = models.DateTimeField(blank=True, null=True)
    author = models.ForeignKey(settings.AUTH_USER_MODEL,
                               on_delete=models.CASCADE,
                               related_name="posts",
                               null=True)    
    
    tags = models.ManyToManyField('tags.Tag', related_name="posts", blank=True)
    category = models.ForeignKey('categories.Category',
                                 on_delete=models.CASCADE,
                                 related_name="posts",
                                 null=True)    

    score = models.IntegerField(default=0)


    TYPES = (
        ("article", "Article"),
        ("book", "Book"),        
        ("video", "Video"),
        # ("course", "Course"),        
    )    
    LEVELS = (
        ("all", "All"),
        ("beginner", "Beginner"),
        ("intermediate", "Intermediate"),
        ("advanced", "Advanced"),                
    )
    PRICES = (
        ("free", "Free"),
        ("paid", "Paid"),
    )    

    post_type = models.CharField(default="video", max_length=64, choices=TYPES, blank=True)    
    post_level = models.CharField(default="all", max_length=64, choices=LEVELS, blank=True)
    post_price = models.CharField(default="free", max_length=64, choices=PRICES, blank=True)    



    def __str__(self):
        return self.title

    @permalink
    def get_absolute_url(self):
        return ('post-detail', None, {'slug': self.slug })





    def save(self, *args, **kwargs):
        if not self.id:
            self.pub_date = datetime.datetime.now()

        if self.pk is None:            
            self.slug = slugify(self.title)
                    
        return super(Post, self).save(*args, **kwargs)
    
    
