from django.db import models
from BlogUser.models import CustomUser

class Category(models.Model):
    title = models.CharField(max_length=255)
    back_img = models.ImageField(upload_to='Uploads/Category_Img', blank=True, null=True)
    slug = models.SlugField(unique=True, blank=True)
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)

    def __str__(self):
        return self.title
    
class Blog_Detail(models.Model):
    header_image = models.ImageField(upload_to='Uploads/Blog_Img', blank=True, null=True)
    slug = models.SlugField(unique=True, blank=True)
    category = models.ForeignKey(Category,related_name='Blog', on_delete=models.CASCADE)
    author = models.ForeignKey(CustomUser,on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    description = models.TextField()
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)

    def __str__(self):
        return self.title
    
class Comments(models.Model):
    blog_id = models.ForeignKey(Blog_Detail,related_name='comments', on_delete=models.CASCADE, blank=True, null=True)
    username = models.CharField(max_length=255)
    email = models.EmailField(max_length=255)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.username + " " + self.email

class Reply(models.Model):
    comment = models.ForeignKey(Comments,related_name='relies', on_delete=models.CASCADE, blank=True, null=True)
    username = models.CharField(max_length=255)
    email = models.EmailField(max_length=255)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.username + " " + self.email
