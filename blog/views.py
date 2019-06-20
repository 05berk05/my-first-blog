from django.shortcuts import redirect
from django.shortcuts import render
from django.utils import timezone
from .models import Post
from django.shortcuts import render, get_object_or_404
from .forms import PostForm,UserForm
from django.contrib.auth.mixins import LoginRequiredMixin


# from django.contrib.auth import authenticate, login, logout
# from django.http import HttpResponseRedirect, HttpResponse
# from django.urls import reverse
# from django.contrib.auth.decorators import login_required
from django.views.generic import CreateView, UpdateView,FormView, DeleteView, ListView, DetailView

from django.contrib.auth.models import User


def post_new(request):
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.published_date = timezone.now()
            post.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm()
    return render(request, 'blog/post_edit.html', {'form': form})
# def post_new(request):
#     form = PostForm()
#     return render(request, 'blog/post_edit.html', {'form': form})

def post_list(request):
     posts = Post.objects.filter(published_date__lte=timezone.now()).order_by('published_date')
     return render(request, 'blog/post_list.html', {'posts': posts})

def post_detail(request, pk):
     post = get_object_or_404(Post, pk=pk)
     return render(request, 'blog/post_detail.html', {'post': post})

# class BlogCreateView(CreateView):
#     model = Blog
#     template_name = ".html"
#     # form_class=ModelCreateForm


def post_edit(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.published_date = timezone.now()
            post.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm(instance=post)
    return render(request, 'blog/post_edit.html', {'form': form})

def hello(request):
    return render(request, 'blog/hello.html', {'hellos': "bloğuma hoş geldin"})

def post_delete(request,pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        print(request.method)
        form = PostForm(request.POST)
        post.delete()
        if form.is_valid():
            messages.success(request, "you have successfully deleted the post {{ post.title }}") #nasıl pk atanır sor, hangi post yani
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm(instance=post)
    posts = Post.objects.all().order_by('published_date')
    return render(request, 'blog/post_list.html', {'posts': posts}) #bu sırasıyla request template context oluyor

# class RequestDeleteView(MessageMixin, DeleteView):
#     """
#     Sub-class the DeleteView to restrict a User from deleting other 
#     user's data.
#     """
#     success_message = "Deleted Successfully"

#     def get_queryset(self):
#         qs = super(RequestDeleteView, self).get_queryset()
#         return qs.filter(owner=self.request.user)
    


class PostDeleteView(DeleteView):
    def get_context_data(self, **kwargs):
        context = super(PostDeleteView, self).get_context_data(**kwargs)
        context["user"] = request.user 
        return context
    model = Post
    template_name = "post_list.html"

# #login logout
# def index(request):
#     return render(request,'dappx/index.html')
# @login_required
# def special(request):
#     return HttpResponse("You are logged in !")
# @login_required
# def user_logout(request):
#     logout(request)
#     return HttpResponseRedirect(reverse('index'))
# def register(request):
#     registered = False
#     if request.method == 'POST':
#         user_form = UserForm(data=requ(data=request.POST)
#         # if user_form.is_valid() and profile_form.is_valid():
#         #     user = user_form.save()
#         #     user.set_password(user.password)
#         #     user.save()
#         #     profile = profile_form.save(commit=False)
#         #     profile.user = user
#         #     if 'profile_pic' in request.FILES:
#         #         print('found it')
#         #         profile.profile_pic = request.FILES['profile_pic']
#         #     profile.save()
#         #     registered = True
#         # else:
#         #     print(user_form.errors,profile_form.errors)
#     else:
#         user_form = U()
#     return render(request,'dappx/registration.html',
#                           {'user_form':user_form,
#                            'profile_form':profile_form,
#                            'registered':registered})
# def user_login(request):
#     if request.method == 'POST':
#         username = request.POST.get('username')
#         password = request.POST.get('password')
#         user = authenticate(username=username, password=password)
#         if user:
#             if user.is_active:
#                 login(request,user)
#                 return HttpResponseRedirect(reverse('index'))
#             else:
#                 return HttpResponse("Your account was inactive.")
#         else:
#             print("Someone tried to login and failed.")
#             print("They used username: {} and password: {}".format(username,password))
#             return HttpResponse("Invalid login details given")
#     else:
#         return render(request, 'dappx/login.html', {})



class CreateUserView (FormView):
    model = User
    template_name = "blog/createuser.html"
    success_url='/'
    form_class = UserForm

    def form_valid(self,form):
        print(self.request.POST)
        response= super(CreateUserView,self).form_valid(form)
        user, created = User.objects.get_or_create(username=form.instance.username,first_name=form.instance.first_name,last_name=form.instance.last_name)
        user.set_password(form.instance.password)
        user.save()
        return response

class BlogListView(LoginRequiredMixin,ListView):
    model = Post
    template_name = "blog/listview.html"
    context_object_name = "blogs"

    def get_queryset(self):
        queryset = super(BlogListView, self).get_queryset()
        queryset = queryset.filter(  author =self.request.user)
        print(list(queryset))
        return queryset

