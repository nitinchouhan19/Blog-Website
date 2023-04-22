from django.urls import path,include
from . import views
urlpatterns = [
    path('',views.index,name = 'index'),
    path('category/<str:pk>',views.category ,name = 'category'),


    path('blog/<str:pk>',views.getBlog,name = 'getBlog'),
    path('myBlogs',views.getmyBlog,name = 'myBlogs'),
    path('myBlogs/delete/<str:pk>',views.deleteBlog,name = 'delete'),
    path('myBlogs/edit/<str:pk>',views.editBlog,name ='edit'),
    path('myBlogs/create',views.create ,name = 'create'),
    path('myBlogs/draft',views.draftBlog ,name = 'draft'),

    path('profile/<str:pk>',views.profile,name = 'profile'),
    path('profile/',views.myprofile,name = 'myprofile'),

    path('search/',views.search,name = 'search'),

    path('login',views.login,name = 'login'),
    path('logout',views.logout_view,name = 'logout'),
    path('register',views.register,name = 'register'),
]