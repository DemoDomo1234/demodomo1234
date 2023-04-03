from django.db import models
from accounts.models import User
from django.urls import reverse
from django.contrib.contenttypes.fields import GenericRelation
from coments.models import Coments



class Post(models.Model):
    body = models.TextField()
    likes = models.ManyToManyField(User, related_name = 'likes_post', blank= True)
    unlikes = models.ManyToManyField(User, related_name = 'unlikess_post', blank= True)
    time = models.DateTimeField(auto_now_add=True )
    user = models.ForeignKey(User, related_name= 'users_post', on_delete=models.CASCADE , default=True)
    comments = GenericRelation(Coments)
    views = models.ManyToManyField(User, related_name = 'views_post', blank= True)

    def __str__(self):
        return self.body
        
    def get_absolute_url(self):
        return reverse("blog:BlogDetail",args=[self.id] )


class Image(models.Model):
    post = models.ForeignKey(Post , related_name="post_images" , on_delete = models.CASCADE , null =  True , blank = True)
    image = models.ImageField( upload_to='media' , null =  True , blank = True)
    time = models.DateTimeField(auto_now_add=True )

    def get_absolute_url(self):
        return reverse("blog:BlogList")
        