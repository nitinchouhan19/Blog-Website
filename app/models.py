from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete = models.CASCADE)
    profile = models.URLField(default='https://cdn-icons-png.flaticon.com/512/727/727399.png?w=740&t=st=1680948461~exp=1680949061~hmac=a6153e0bfcf0730e196145ccdc2e65f2bdfcac9326644563ff812bdf2b3fc0cd')
    email = models.EmailField(unique=True, null=True)
    description = models.TextField(null = True)

    def __str__(self):
        return self.user.username
    
class Category(models.Model):
    name = models.CharField(max_length=30)
    image = models.URLField()
    description = models.TextField()

    def __str__(self):
        return self.name


class Blog(models.Model):
    title = models.CharField(max_length=200, unique=False)
    author = models.ForeignKey(Profile, on_delete= models.CASCADE)
    updated_on = models.DateTimeField(auto_now= True)
    content = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)
    image = models.URLField(null=True)
    is_posted = models.BooleanField(default=False)
    category = models.ForeignKey(Category,on_delete=models.CASCADE,null = True)


    def __str__(self):
        return self.title
    
class Favourite(models.Model):
    blog_id = models.ForeignKey(Blog, on_delete= models.CASCADE)
    user_id = models.OneToOneField(Profile, on_delete= models.CASCADE)

    def __str__(self):
        return self.user_id.user.username + "'s Favourite Blog"
    

class Comment(models.Model):
    blog = models.ForeignKey(Blog,on_delete=models.CASCADE,related_name='comments')
    name = models.ForeignKey(Profile,on_delete = models.CASCADE,null = True)
    body = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.body