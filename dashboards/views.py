from turtle import title
import uuid
from django.db.models.query import InstanceCheckMeta
from django.http import Http404, request
from django.template import context
from blogs.models import Blog, category
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required, permission_required
from .forms import AddUserForm, BlogPostForm, CategoryForm, EditUserForm
from django.template.defaultfilters import slugify
from django.contrib.auth.models import User

# Create your views here.
@login_required(login_url='login')
def dashboard(request):
  category_count = category.objects.all().count()
  blogs_count =Blog.objects.all().count()
  
  context= {
    'category_count': category_count,
    'blogs_count': blogs_count,
  }
  
  return render(request, 'dashboard/dashboard.html', context)

def categories(request):
  return render(request, 'dashboard/categories.html')

@login_required
@permission_required('blogs.add_category', raise_exception=True)
def add_category(request):
  if request.method == 'POST':
    form = CategoryForm(request.POST)
    if form.is_valid():
      form.save()
      return redirect('categories')
  form = CategoryForm()
  context = {
    'form':form,
  }
  return render(request, 'dashboard/add_category.html', context)

@login_required
@permission_required('blogs.change_category', raise_exception=True)
def edit_category(request, pk):
  Category = get_object_or_404(category, pk=pk)
  if request.method == 'POST':
    form = CategoryForm(request.POST, instance=Category)
    if form.is_valid():
      form.save()
      return redirect('categories')
  form = CategoryForm(instance=Category)
  context = {
    'form': form,
    'Category': Category,
  }
  return render(request, 'dashboard/edit_category.html', context)
  
@login_required
@permission_required('blogs.delete_category', raise_exception=True)
def delete_category(request, pk):
  Category = get_object_or_404(category, pk=pk)
  Category.delete()
  return redirect('categories')


@login_required
def posts(request):
  posts = Blog.objects.all()
  context = {
    'posts': posts
  }
  return render(request, 'dashboard/posts.html', context)

@login_required
@permission_required('blogs.add_blog', raise_exception=True)
def add_post(request):
  if request.method == 'POST':
    form = BlogPostForm(request.POST, request.FILES)
    if form.is_valid():
      title = form.cleaned_data['title']
      post = form.save(commit=False)
      post.author = request.user
      # Set unique slug before first save (empty slug would violate UNIQUE)
      post.slug = slugify(title) + '-' + str(uuid.uuid4())[:8]
      post.save()
      post.slug = slugify(title) + '-' + str(post.id)
      post.save(update_fields=['slug'])
      return redirect('posts')
    else:
      print('form is invalid')
      print(form.errors)
  form = BlogPostForm()
  context = {
    'form': form,
  }
  return render(request, 'dashboard/add_post.html', context)



@login_required
@permission_required('blogs.change_blog', raise_exception=True)
def edit_post(request, pk):
  post = get_object_or_404(Blog, pk=pk)
  
  if request.method == 'POST':
    form = BlogPostForm(request.POST, request.FILES, instance=post)
    if form.is_valid():
      post = form.save()
      title = form.cleaned_data['title']
      post.slug = slugify(title) + '-'+str(post.id)
      post.save()
      return redirect('posts')
  form = BlogPostForm(instance=post)
  context = {
    'form':form,
    'post':post,
  }
  return render(request, 'dashboard/edit_post.html', context)


@login_required
@permission_required('blogs.delete_blog', raise_exception=True)
def delete_post(request, pk):
  post = get_object_or_404(Blog, pk=pk)
  post.delete()
  return redirect('posts')


def users(request):
  users = User.objects.all()
  context = {
    'users': users,
  }
  return render(request, 'dashboard/users.html', context)


def add_user(request):
  if request.method == 'POST':
    form = AddUserForm(request.POST)
    if form.is_valid():
      form.save()
      return redirect('users')
    else:
      print(form.errors)
  form = AddUserForm()
  context ={
    'form':form,
  }
  return render(request, 'dashboard/add_user.html', context)



def edit_user(request, pk):
  user = get_object_or_404(User, pk=pk)
  if request.method == 'POST':
    form = EditUserForm(request.POST, instance=user)
    if form.is_valid():
      form.save()
      return redirect('users')
  form = EditUserForm(instance=user)
  context = {
    'form': form,
  }
  return render(request, 'dashboard/edit_user.html', context)



def delete_user(request, pk):
  user = get_object_or_404(User, pk=pk)
  user.delete()
  return redirect('users')