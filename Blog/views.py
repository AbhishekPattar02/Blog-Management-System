from django.shortcuts import render,redirect
from django.urls import reverse
from django.contrib import messages
from django.core.mail import send_mail, BadHeaderError
from django.core.paginator import Paginator
from django.conf import settings
from BlogUser.models import *
from .models import *

def Blog_Home(request):
    Categories = Category.objects.all()
    latest_blog = Blog_Detail.objects.all().order_by('-created_at')[:5]

    category_Blog ={}
    for categories in Categories:
        blogs = Blog_Detail.objects.filter(category=categories).order_by('-created_at')[:3]
        category_Blog[categories] = blogs
    
    
    context = {
        'Categories':Categories,
        'latest_blog':latest_blog,
        'category_Blog':category_Blog,
    }
    return render(request,'Blog/Blog_Home.html',context)

def Blog_Latest(request):
    Categories = Category.objects.all()
    latest_blog = Blog_Detail.objects.all().order_by('-created_at')[:9]
    
    paginator = Paginator(latest_blog,3)
    page_number = request.GET.get('page')
    Blogs = paginator.get_page(page_number)
    total_page = Blogs.paginator.num_pages

    context = {
        'Categories':Categories,
        'Blogs' : Blogs,
        'total_page' : [n+1 for n in range(total_page)],
    }
    return render(request,'Blog/Blog_Latest.html',context)
 
def Blog_List(request,slug):
    Categories = Category.objects.all()
    category_slug = Category.objects.get(slug =slug)
    Category_Blog = Blog_Detail.objects.filter(category = category_slug )

    paginator = Paginator(Category_Blog,3)
    page_number = request.GET.get('page')
    Blogs = paginator.get_page(page_number)
    total_page = Blogs.paginator.num_pages

    context = {
        'Categories':Categories,
        'category_slug':category_slug,
        'Blogs' : Blogs,
        'total_page' : [n+1 for n in range(total_page)],
    }
    return render(request,'Blog/Blog_List.html',context)

def Blog_Details(request,slug):
    Categories = Category.objects.all()

    Blog = Blog_Detail.objects.get(slug=slug)

    comments = Comments.objects.filter(blog_id=Blog).order_by('-created_at')[:3]

    action = request.GET.get('action')
    reply = Reply.objects.filter(comment=action)
    context = {
        'Categories':Categories,
        'Blog':Blog,
        'comments':comments,
        'action' :action,
        'reply' :reply,
    }
    return render(request,'Blog/Blog_Details.html',context)


def Save_Comments(request,slug):
    if request.method == "POST":
        name = request.POST.get('name')
        email = request.POST.get('email')
        message = request.POST.get('message')
        Blog = Blog_Detail.objects.get(slug=slug)

        coments = Comments(
            blog_id = Blog,
            username = name,
            email = email,
            message = message,
        )
        coments.save()
        messages.success(request, "Your comment has been added successfully.")
    else:
        messages.error(request, "Failed to add comment. Please try again.")

    return redirect(reverse('Blog-Details', kwargs={'slug':slug}))

def Save_Reply(request,comment_id):
    comment = Comments.objects.get(id=comment_id)

    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        message = request.POST.get('message')
        reply = Reply(
            comment = comment,
            username = name,
            email = email,
            message = message,
        )
        reply.save()
        messages.success(request, "Successfully replied.")
    else:
        messages.error(request, "Failed to reply. Please try again.")

    return redirect('Blog-Details', comment.blog_id.slug)

def Blog_Contact(request):
    Categories = Category.objects.all()
    context = {
        'Categories':Categories
    }
    return render(request,'Blog/Blog_Contact.html',context)

def Save_Contact(request):
    if request.method == "POST":
        name = request.POST.get('name')
        email = request.POST.get('email')
        subject = request.POST.get('subject')
        message = request.POST.get('message')

        contact = Contact(
            name = name,
            email = email,
            subject = subject,
            message = message,
        )
        contact.save()
        try:
            send_mail(subject, message, email, ['yashsp0712@gmail.com'],fail_silently=False)
        except BadHeaderError:
            messages.error('Invalid header found.')
            return redirect('Blog-Contact')
        
        messages.success(request, "Your message has been sent successfully.")
    else:
        messages.error(request, "Failed to send message. Please try again.")

    return redirect('Blog-Contact')

def Search_Blog(request):
    query = request.GET['query']
    Categories = Category.objects.all()
    Search_blog = Blog_Detail.objects.filter(title__icontains = query )

    paginator = Paginator(Search_blog,3)
    page_number = request.GET.get('page')
    Blogs = paginator.get_page(page_number)
    total_page = Blogs.paginator.num_pages  
    context = {
        'Categories' : Categories,
        'Blogs' : Blogs,
        'total_page' : [n+1 for n in range(total_page)],
    }
    
    return render(request,"Blog/Blog_Search.html",context)