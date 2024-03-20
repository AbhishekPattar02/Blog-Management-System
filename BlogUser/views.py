from django.shortcuts import render,redirect
from django.contrib.auth import login, authenticate,logout
from django.contrib.auth.decorators import login_required
from django.utils.text import slugify
from django.contrib import messages
from django.core.paginator import Paginator

from .models import *
from Blog.models import *

def User_Login(request):
    return render(request,"BlogUser/User_Login.html")

def User_Register(request):
    return render(request,"BlogUser/User_Register.html")

def do_Register(request):
    if request.method == "POST":
        first_name = request.POST.get('Fname') 
        last_name = request.POST.get('Lname')
        email = request.POST.get('Email')
        username = request.POST.get('Username')
        password = request.POST.get('Password')
        confirm_password = request.POST.get('Cpassword')

        if password != confirm_password:
            messages.error(request, "Passwords do not match.")
            return redirect("User-Register")
        
        user = CustomUser(
            first_name  = first_name,
            last_name = last_name,
            email = email,
            username = username,
            user_type = 2
        )

        user.set_password(password)
        user.save()
        messages.success(request, "Registration successful.")
        return redirect("User-Login")

def do_Login(request):
    if request.method == "POST":
        username = request.POST.get('Username')
        password = request.POST.get('Password')

        user = authenticate(request,
                            username=username,
                            password=password
                            )
        
        if user is not None:
            login(request, user)
            user_type = user.user_type

            if user_type == '1':
                return redirect("admin")
            
            elif user_type == '2':
                return redirect("Blog_Home")
            
            else:
                messages.error(request, "Invalid user type.")
                return redirect("User-Login")
            
        else:
            messages.error(request, "Invalid username or password.")
            return redirect('User-Login')

@login_required(login_url="User-Login")
def User_Logout(request):
    logout(request)
    return redirect('Blog_Home') 

@login_required(login_url="User-Login")
def View_Profile(request):
    user = CustomUser.objects.get( id = request.user.id )
    Categories = Category.objects.all()
    context = {
        'Categories':Categories,
        'user' : user,
    }
    return render(request,"BlogUser/View_Profile.html",context)

@login_required(login_url="User-Login")
def Update_Profile(request):
    if request.method == "POST":
        first_name = request.POST.get('First_name') 
        last_name = request.POST.get('Last_name')
        password = request.POST.get('Password')
        profile_pic = request.FILES.get('Profile_pic')

        user = CustomUser.objects.get( id = request.user.id )
        
        user.first_name  = first_name
        user.last_name = last_name

        if profile_pic != None and profile_pic != '':
            user.profile_pic = profile_pic

        if password != None and password != '':
            user.set_password(password)
        
        user.save()
        messages.success(request, "Profile updated successfully.")
        return redirect("View-Profile")
    
@login_required(login_url="User-Login")
def Add_Blog(request):
    Categories = Category.objects.all()
    category = Category.objects.all()
    user = CustomUser.objects.get( id = request.user.id )
    context ={
        'Categories':Categories,
        'category':category,
        'user' : user,
    }
    return render(request,"BlogUser/Add_Blog.html",context)

@login_required(login_url="User-Login")
def Save_Blog(request):
    user = CustomUser.objects.get(id=request.user.id)
    if request.method == "POST":
        Header_img = request.FILES.get('Header_img')
        category_id = request.POST.get('category')
        blog_Title = request.POST.get('Title')
        blog_dtail = request.POST.get('Blog_Detail')
        author = user
        slug = slugify(blog_Title)
        category = Category.objects.get(id = category_id)

        blog = Blog_Detail(
            header_image = Header_img,
            slug = slug,
            category = category,
            author = author,
            title = blog_Title,
            description = blog_dtail,
        )
        blog.save()
        messages.success(request, "Blog saved successfully.")
    else:
        messages.error(request, "Failed to save the blog.")

    return redirect('Add-Blog')
    
@login_required(login_url="User-Login")
def View_Blog(request):
    Categories = Category.objects.all()
    user = CustomUser.objects.get(id=request.user.id)
    blog = Blog_Detail.objects.filter(author = user)
    user = CustomUser.objects.get( id = request.user.id )

    paginator = Paginator(blog,3)
    page_number = request.GET.get('page')
    Blogs = paginator.get_page(page_number)
    total_page = Blogs.paginator.num_pages
    context={
        'Categories':Categories,
        'Blogs' : Blogs,
        'user' : user,
        'total_page' : [n+1 for n in range(total_page)],
    }
    return render(request,"BlogUser/View_Blog.html",context)

@login_required(login_url="User-Login")
def Edit_Blog(request,slug):
    Categories = Category.objects.all()
    category = Category.objects.all()
    Blog = Blog_Detail.objects.get( slug = slug )
    user = CustomUser.objects.get( id = request.user.id )
    context ={
        'Categories':Categories,
        'category':category,
        'user' : user,
        'Blog' :Blog
    }
    return render(request,"BlogUser/Edit_Blog.html",context)

@login_required(login_url="User-Login")
def Update_Blog(request,slug):
    user = CustomUser.objects.get(id=request.user.id)
    blog = Blog_Detail.objects.get(slug=slug, author=user)
    if request.method == "POST":
        Header_img = request.FILES.get('Header_img')
        category_id = request.POST.get('category')
        blog_Title = request.POST.get('Title')
        blog_dtail = request.POST.get('Blog_Detail')
        author = user
        slug = slugify(blog_Title)
        category = Category.objects.get(id = category_id)

        blog.slug = slug
        blog.category = category
        blog.author = author
        blog.title = blog_Title
        blog.description = blog_dtail
        if Header_img != None and Header_img != '':
            blog.header_image = Header_img
        blog.save()
        messages.success(request, "Blog updated successfully.")
    else:
        messages.error(request, "Failed to update the blog.")

    return redirect('View-Blog')

@login_required(login_url="User-Login")
def Delete_Blog(request, slug):
    try:
        blog = Blog_Detail.objects.get(slug=slug)
        blog.delete()
        messages.success(request, "Blog deleted successfully.")
    except Blog_Detail.DoesNotExist:
        messages.error(request, "Blog does not exist.")

    return redirect('View-Blog')