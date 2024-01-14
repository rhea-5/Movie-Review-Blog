from django.db import models
from django.contrib.auth.models import User

#use superuser created

STATUS=((0,"Draft"),(1,"Published"))

class Post(models.Model):
    title=models.CharField(max_length=255, unique=True)
    author=models.ForeignKey(User,on_delete=models.CASCADE)
    #after deleting the author, their posts get deleted
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    content = models.TextField(max_length=2000)
    status = models.IntegerField(choices=STATUS, default=0)
    

class Meta:
    ordering=['-created_on']

def __str__(self):
        return self.title + ' | ' + str(self.author)

# Create your models here.
