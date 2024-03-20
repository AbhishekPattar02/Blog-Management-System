from django.urls import path
from . import views 

urlpatterns = [
    path('Login',views.User_Login , name="User-Login"),
    path('Register',views.User_Register , name="User-Register"),
    path('Logout',views.User_Logout , name="User-Logout"),

    path('do_Register',views.do_Register , name="Do-Register"),
    path('do_Login',views.do_Login , name="Do-Login"),

    path('Profile',views.View_Profile , name="View-Profile"),
    path('Update_Profile',views.Update_Profile , name="Update-Profile"),
    
    path('Add_Blog',views.Add_Blog,name="Add-Blog"),
    path('Save_Blog',views.Save_Blog,name="Save-Blog"),
    path('View_Blog',views.View_Blog,name="View-Blog"),
    path('Edit_Blog/<slug:slug>',views.Edit_Blog,name="Edit-Blog"),
    path('Update_Blog/<slug:slug>',views.Update_Blog,name="Update-Blog"),
    path('Delete_Blog/<slug:slug>',views.Delete_Blog,name="Delete-Blog"),

]
