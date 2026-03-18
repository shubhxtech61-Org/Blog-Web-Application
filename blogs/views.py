from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect, render
from blogs.models import Blog, category, Comment
from django.db.models import Q

# Create your views here.
def posts_by_category(request, category_id): 
    posts = Blog.objects.filter(status='Published', category=category_id)#fetch the post that belong to the category with the id category_id
    try:# use try/except when we wants to do some custom action if the category does not exists
        Category=category.objects.get(pk=category_id)
    except: #it will redirect the user to home page if category does not exist
        return redirect('home')  
    #use get_object_or_404 when u want to show 404 error page if category does not exist
    # category = get_object_or_404(category, pk=category_id)
    
    
    context = {
        'posts': posts,
        'Category': Category,
    }
    return render(request, 'posts_by_category.html', context)


def blogs(request, slug):
    single_blog= get_object_or_404(Blog, slug=slug, status='Published')
    if request.method == 'POST':
        comment = Comment()
        comment.user = request.user
        comment.blog = single_blog
        comment.comment = request.POST['comment']
        comment.save()
        return HttpResponseRedirect(request.path_info)
    
    #Comments
    comments = Comment.objects.filter(blog=single_blog)
    comments_count = comments.count()
    
    context = {
        'single_blog': single_blog,
        'comments': comments,
        'comments_count': comments_count,
    }
    return render(request, 'blogs.html', context)

def search(request):
    keyword = request.GET.get('keywords')
    blogs = Blog.objects.filter(Q(title__icontains = keyword) | Q(short_description__icontains = keyword) | Q(blog_body__icontains = keyword), status='Published')
    context = {
        'blogs': blogs,
        'keyword':keyword,
    }
    return render(request, 'search.html', context)