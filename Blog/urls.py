from django.urls import path
from . import views

urlpatterns = [
    path('',views.Blog_Home, name='Blog_Home'),
    path('Blog/Category/<slug:slug>',views.Blog_List, name='Blog-List'),
    path('Blog/Detail/<slug:slug>',views.Blog_Details, name='Blog-Details'),

    path('Blog_Contact',views.Blog_Contact, name='Blog-Contact'),
    path('Save_Contact',views.Save_Contact, name='Save-Contact'),

    path('Save_Comments/<slug:slug>',views.Save_Comments, name='Save-Comments'),
    path('Save_Reply/<int:comment_id>',views.Save_Reply, name='Save-Reply'),
   
    path('Blog_Latest',views.Blog_Latest, name='Blog-Latest'),
    path('Search_Blog',views.Search_Blog, name='Search-Blog'),

]
