from django.db import models
from django.db.models import permalink

class Tag(models.Model):
    title = models.CharField(max_length=64)    
    slug = models.SlugField(max_length=64, default="")

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super(Tag, self).save(*args, **kwargs)

        
    @permalink
    def get_absolute_url(self):
        return ('view_tag', None, {'slug': self.slug })
