#===========================
#blog/models.py
#===========================
#--------------------------------------------------
#IMPORTS
from django.db import models
from django.utils import timezone
from django.urls import reverse

#####################################################
#Classes
#####################################################
#--------------------------------------------------
#Class: Post
#takes: author, title, text, creation date, and publish date
class Post(models.Model):
    author = models.ForeignKey('auth.User')
    title = models.CharField(maxlength=200)
    text = models.TextField()
    create_date = models.DateField(default=timezone.now())
    published_date = models.DateField(blank=True,null=True)

    #method: publish
    #publish post
    def publish(self):
        self.published_date = timezone.now()
        self.save()

    #method: approve_comments
    #give poster/admin ability to approve/decline specific comments
    def approve_comments(self):
        return self.comments.filter(approved_comment=True)

    #method: get_absolute_url
    #return to the post details page
    def get_absolute_url(self):
        return reverse('post_detail', kwargs={'pk':self.pk})

    def __str__(self):
        return self.title

#--------------------------------------------------
#Class: Comment
#takes: post, author, text, creation date, and approved_comment
class Comment(models.Model):
    post = models.ForeignKey('blog.Post', related_name='comments')
    author = models.CharField(maxlength=200)
    text = models.TextField()
    create_date = models.DateField(default=timezone.now())
    approved_comment = models.BooleanField(default=False)

    #method: approve
    #give poster/admin ability to approve/decline specific comments
    def approve(self):
        self.approved_comment = True
        self.save()

    #method: get_absolute_url
    #return to the post list page
    def get_absolute_url(self):
        return reverse('post_list')

    def __str__():
        return self.text
