from django.shortcuts import render,redirect
from .models import *
from django.contrib.auth import authenticate
from django.contrib.auth import login as dj_login
from django.contrib.auth import logout 
from django.contrib import messages
from django.db.models import Q
from .forms import BlogForm
from django.contrib.auth.decorators import login_required
# Create your views here.
def index(request):
    categories = Category.objects.all()
    blogs = Blog.objects.filter(is_posted = True)
    context = {'blogs':blogs,'search':search,'categories':categories}
    return render(request,'index.html',context)

def search(request):
    if request.method == 'GET' and request.GET.get('query')!= None:
        query = request.GET.get('query') if request.GET.get('query')!= None else ''
        try:
            category = Category.objects.get(name__iexact = query)
            if category :
                blogs = Blog.objects.filter(category = category , is_posted = True)
                context = {'blogs':blogs,'category':category}
                return render(request,'category.html',context)
        except :
            blogs = Blog.objects.filter(
                Q( title__icontains = query)|
                Q( content__icontains = query)|
                Q(author__user__username__icontains = query)|
                Q( category__name__icontains = query)
            )
            blog_list = []
            for blog in blogs :
                if blog.is_posted == True:
                    blog_list.append(blog)
            context = {'blogs': blog_list, 'search':search}
            return render(request,'search_result.html',context)
    return redirect('index')
    

def category(request,pk):
    category = Category.objects.get(id = pk )
    blogs = Blog.objects.filter(category = category)
    print(blogs)
    context = {'blogs':blogs,'category':category}
    return render(request,'category.html',context)


def getBlog(request,pk):
    if request.method == 'GET' and request.GET.get('review') is not None:
        blog = Blog.objects.get(id = pk)
        
        profile = Profile.objects.get(user=request.user)
        if profile == blog.author:
            message = "Author of blog is not allowed to write reviews"
            blog = Blog.objects.get(id = pk)
            reviews = Comment.objects.filter(blog = blog).order_by('-created_on')
            context = {'blog': blog ,'reviews':reviews ,'message':message}
            return render(request,'blog.html',context)
            
        if request.GET.get('review') is not None:
            comment = Comment.objects.create(
                name = profile,
                blog = blog,
                body = request.GET.get('review')
            )

        blog = Blog.objects.get(id = pk)
        reviews = Comment.objects.filter(blog = blog).order_by('-created_on')
        context = {'blog': blog ,'reviews':reviews }
        return render(request,'blog.html',context)
    
    blog = Blog.objects.get(id = pk)
    reviews = Comment.objects.filter(blog = blog)
    context = {'blog': blog ,'reviews':reviews }
    return render(request,'blog.html',context)

@login_required(login_url= 'login')
def getmyBlog(request):
    profile = Profile.objects.get(user=request.user)
    blogs = Blog.objects.filter(author = profile)
    myBlogs = "myBlogs"
    context = {'blogs':blogs,'myBlogs': myBlogs}
    return render(request,'index.html',context)

@login_required(login_url= 'login')
def deleteBlog(request,pk):
    blog = Blog.objects.get(id = pk)
    blog.delete()
    return redirect('myBlogs')

@login_required(login_url= 'login')
def editBlog(request,pk):
    if request.method == 'POST' :
        blog = Blog.objects.get(id = pk)
        blog.is_posted = True
        form = BlogForm(request.POST,instance = blog)
        if form.is_valid():
            form.save()
            return redirect('index')
    blog = Blog.objects.get(id = pk)
    form = BlogForm(instance = blog)
    update = "update"
    context = {'form':form,'update': update }
    return render(request,'blog_form.html',context)

@login_required(login_url= 'login')
def create(request):
    if request.method == 'POST' and request.POST.get('title')!=None:
        profile = Profile.objects.get(user = request.user)
        if 'Post_Blog' in request.POST:
            category_id =  request.POST.get('category')
            blog_category = Category.objects.get(id = category_id)
            blog = Blog.objects.create(
                author = profile,
                title = request.POST.get('title'),
                content = request.POST.get('content'),
                image = request.POST.get('image'),
                is_posted = True,
                category = blog_category,
            )
            return redirect('index')
        if 'Draft' in request.POST:
            category_id =  request.POST.get('category')
            blog_category = Category.objects.get(id = category_id)
            blog = Blog.objects.create(
                author = profile,
                title = request.POST.get('title'),
                content = request.POST.get('content'),
                image = request.POST.get('image'),
                is_posted = False,
                category = blog_category,
            )
            return redirect('index')   
    form = BlogForm()
    create = True
    print(create)
    context = {'form':form,'create': create}
    return render(request,'blog_form.html',context)

@login_required(login_url= 'login')
def draftBlog(request):
    profile = Profile.objects.get(user = request.user)
    blogs = Blog.objects.filter(
        is_posted = False,
        author = profile
    )
    mydraft = "mydraft"
    context = {'blogs': blogs,'draft':mydraft}
    return render(request,'draft.html',context)

@login_required(login_url= 'login')
def myprofile(request):
    profile = Profile.objects.get(user = request.user)
    blogs = Blog.objects.filter(author = profile)
    myprofile = "myprofile"
    context = {'blogs':blogs ,'profile': profile,'myprofile': myprofile}
    return render(request,'profile.html',context)

def profile(request,pk):
    profile = Profile.objects.get(id = pk)
    blogs = Blog.objects.filter(author = profile)
    context = {'blogs':blogs ,'profile': profile}
    return render(request,'profile.html',context)

def login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username = username, password = password)

        if user is not None:
            dj_login(request,user)
            return redirect('index')
        else:
            messages.error(request, "Credentials Invalid")
    return render(request, 'login_registration.html')


def logout_view(request):
    logout(request)
    print("!")
    return redirect('index')

def register(request):
  if request.method == 'POST':
    username = request.POST.get('username')
    password = request.POST.get('password')
    confirm_password = request.POST.get('confirm_password')
    email = request.POST.get('email')

    if password == confirm_password :
      user = User.objects.create_user(
        username = username,
        password = password,
        email = email
      )
      profile = Profile.objects.create(
          user = user,
          email = email,
      )
      dj_login(request ,user )
      return redirect('index')
    else:
      messages.error(request,'Enter Details Correctly')
  
  register = "register"
  context = {'register': register}   
  return render(request , 'login_registration.html',context)