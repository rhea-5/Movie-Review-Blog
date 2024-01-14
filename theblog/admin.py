from django.contrib import admin
#register new model
from .models import Post

#add filters to admin page of posts
class PostAdmin(admin.ModelAdmin):
    list_display=('title','status','created_on')
    list_filter=('status',)
    search_fields=['title','content']

#Blog post entries will be accesible to admin (superuser)
admin.site.register(Post, PostAdmin)
# Register your models here.
