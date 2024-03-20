from django.db import models
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    user_type_choices =(
        (1,"Admin"),
        (2,"User")
    )
    user_type= models.CharField(choices=user_type_choices, max_length=50, default=1,null=True)
    profile_pic = models.ImageField(upload_to='Uploads/Profile_Img',  blank=True, null=True)

    def __str__(self):
        return self.first_name + ' ' + self.last_name

class Contact(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField(max_length=255)
    subject = models.CharField(max_length=255)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name + " " + self.email + " " + self.subject 