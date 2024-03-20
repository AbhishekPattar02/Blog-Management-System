from django.contrib import admin
from .models import *

class CategoryAdmin(admin.ModelAdmin):
    list_display = ['title','slug','created_at','updated_at']
    list_filter = ['title']
    prepopulated_fields = {'slug':['title']}
    search_fields  = ['title']

class Blog_DetailAdmin(admin.ModelAdmin):
    list_display = ['category','title','author','slug']
    list_filter = ['category']
    prepopulated_fields = {'slug':['title']}
    search_fields  = ['title','category','author']

admin.site.register(Category,CategoryAdmin)
admin.site.register(Blog_Detail,Blog_DetailAdmin)
admin.site.register(Comments)
admin.site.register(Reply)
# Register your models here.
