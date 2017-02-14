from django.db import models
from django.template.defaultfilters import slugify
from django.conf import settings
from django.db.models import permalink

from posts.models import Post

class Comment(models.Model):
    post = models.ForeignKey('posts.Post', on_delete=models.CASCADE,
                             related_name="comments",
                             default=None, null=True, blank=True)    
    # parent = models.ForeignKey('Comment', related_name="children",
    #                            default=None, null=True, blank=True)
    body = models.TextField()    
    author = models.ForeignKey(settings.AUTH_USER_MODEL,
                               on_delete=models.CASCADE,
                               related_name="comments", default="")
    score = models.IntegerField(default=0)
    pub_date = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        string_name = ""
        try:
            string_name = self.body # self.story.title + self.body
        except:
            string_name = "comment" #self.body # self.chapter.title + self.body
        if len(string_name) > 64:
            string_name = string_name[:64] + "..."
        return string_name
    

    @permalink
    def get_absolute_url(self):
        return ('view_comment', None, { 'story': self.video.slug,
                                            'comment_id': self.id })
        
