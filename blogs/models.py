from django.db import models
from django.contrib.auth.models import User

class Blog(models.Model):
    title = models.CharField(max_length=100)
    desc = models.TextField()
    date_posted = models.DateField()
    is_archived = models.BooleanField(default=False)
    owner = models.ForeignKey(User, on_delete=models.CASCADE) 

    def __str__(self):
        return self.name
    

class Comment(models.Model):
    comment = models.CharField(max_length=100)
    date_commented = models.DateField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE)

class Like(models.Model):
    date_liked = models.DateField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE)

class Notification(models.Model):
    is_read = models.BooleanField()
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE)
    like = models.ForeignKey(Like, on_delete=models.CASCADE)

class Saved(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE)