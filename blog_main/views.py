from django.shortcuts import redirect, render
from assignments.models import About
from blog_main.forms import RegistrationForm
from blogs.models import Blog
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import auth
# Create your views here.

def home(request):
    # don't needed cause be are rendering for the all pages using context processors
    # categories = category.objects.all()#for fetch categories from db
    featured_post = Blog.objects.filter(is_featured=True, status='Published').order_by('-updated_at')
    posts = Blog.objects.filter(is_featured= False, status='Published')
    try:
        about = About.objects.get()
    except:
        about = None
        
    context = {
        # 'categories': categories, #don't needed
        'featured_post': featured_post,
        'posts': posts,
        'about': about,
    }
    return render(request, 'home.html', context)

#  For register Page
def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('register')
        else:
            print(form.errors)
    else:
        form = RegistrationForm()
    context = {
        'form': form
    }
    return render(request, 'register.html', context)

# for login page
def login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            
            user = auth.authenticate(username=username, password=password)
            if  user is not None:
                auth.login(request, user)
            return redirect('dashboard')
    form = AuthenticationForm()
    context = {
        'form': form,
    }
    return render(request, 'login.html', context)

# for logout
def logout(request):
    auth.logout(request)
    return redirect('home')