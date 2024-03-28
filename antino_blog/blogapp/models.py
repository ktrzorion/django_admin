from django.db import models
from authapp.models import MyUser

class Blog(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    author = models.ForeignKey(MyUser, on_delete = models.CASCADE)

class Like(models.Model):
    user = models.ForeignKey(MyUser, on_delete=models.CASCADE)
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE)

class Comment(models.Model):
    user = models.ForeignKey(MyUser, on_delete=models.CASCADE)
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE)
    text = models.TextField()
    tags = models.CharField(max_length=50, default="")
    created_at = models.DateTimeField(auto_now_add=True)