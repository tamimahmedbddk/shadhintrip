from django.shortcuts import get_object_or_404, render, render
from django.http import JsonResponse
from .models import Post, Category, Tag, BackgroundImage
from django.core.paginator import Paginator

def blog_home(request):
    posts = Post.objects.all()
    categories = Category.objects.all()
    tags = Tag.objects.all()
    recent_posts = Post.objects.order_by('-created_on')[:5]
    background_images = BackgroundImage.objects.all()

    # Pagination
    paginator = Paginator(posts, 5)  # Show 10 tours per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'posts': page_obj,
        'page_obj': page_obj,  # Pass the page object for pagination controls
        'categories': categories,
        'tags': tags,
        'recent_posts': recent_posts,
        'background_images': background_images,
    }
    return render(request, 'blog/index.html', context)


def fetch_blog_posts(request):
    # Get the parameters sent in the AJAX request
    category_id = request.GET.get('category_id')
    tag_id = request.GET.get('tag_id')
    search_term = request.GET.get('search_term')

    # Query the database to retrieve blog posts based on the parameters
    blog_posts = Post.objects.all()

    if category_id:
        blog_posts = blog_posts.filter(category_id=category_id)
    if tag_id:
        blog_posts = blog_posts.filter(tags__id=tag_id)
    if search_term:
        blog_posts = blog_posts.filter(title__icontains=search_term)

    serialized_posts = [{'title': post.title, 'content': post.content} for post in blog_posts]


    response_data = {
        'posts': serialized_posts,
    }

    return JsonResponse(response_data)


def blog_details(request, slug):
    blog_details = get_object_or_404(Post, slug=slug)
    blog_others = Post.objects.all()[:3]
    context = {
        'blog_details': blog_details,
        'blog_others': blog_others,
    }
    return render(request, 'blog/post-details.html', context)

