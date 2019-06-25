from django.contrib import admin
from django.urls import path, include # new include ve virgül yeni bir de üstteki adminli olan
from django.views.generic.base import TemplateView # new
from blog import views
from .views import *


urlpatterns = [
    #path('admin/', admin.site.urls),#new
    #path('blog/', include('blog.urls')), #new
    #path('', TemplateView.as_view(template_name='home.html'), name='home'), #new
    #path('',views.home, name='home'),
    path('', Home.as_view(), name='home'),
    path('posts/', views.post_list, name='post_list'),
    path('post/<int:pk>/', views.post_detail, name='post_detail'),
    path('post/new/', views.post_new, name='post_new'),
    path('post/<int:pk>/edit/', views.post_edit, name='post_edit'),
    path('post/<int:pk>/delete/', views.post_delete, name='delete'),
    path('hello/', views.hello, name='hellos'),
    path('createuserview/', CreateUserView.as_view(), name='createuserview'),
    path("blogs/", BlogListView.as_view(), name="BlogListView"),
    path('accounts/', include('django.contrib.auth.urls')), # new
    path('createuserview/', CreateUserView.as_view(), name='createuserview'),
    path('test/', views.test, name= 'test'),
    


]






