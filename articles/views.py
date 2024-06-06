from django.http import Http404, HttpResponse, JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from articles.models import Members, Post, Image, Category, Role
from django.core.paginator import Paginator
from datetime import datetime

# Create your views here.

def index(request):
    search_query = request.GET.get('search', '')
    items = Post.objects.filter(title__icontains=search_query).order_by('-publication_date')  # Adjust the filter to your needs

    paginator = Paginator(items, 10)  # Show 10 items per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    category = Category.objects.all().order_by('-id')
    posts =  Post.objects.all().order_by('-publication_date')
    context = {
        'page_obj': page_obj,
        'search_query': search_query,
        'category': category,
        'posts': posts,
        'year': datetime.now().year,
    }

    return render(request, 'base.html', context)


def login_view(request):
    authenticated = request.session.get('authenticated', False)
    if authenticated:
        if request.user.is_staff:
            return redirect('admin_members')
        return HttpResponse("you are not admin to access this page")
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        print(user, username, password)
        if user is not None:
            login(request, user)
            request.session['authenticated'] = True
            request.session['username'] = user.username
            if request.user.is_staff:
                return redirect('admin_members')
            else:
               return HttpResponse("you are not admin to access this page")
        else:
            error_message = "Invalid credentials. Please try again."
            return render(request, 'login.html', {'error_message': error_message})

    return render(request, 'login.html')


def admin_members(request):
    authenticated = request.session.get('authenticated', False)
    username = request.session.get('username', None)
    if authenticated:
        if request.user.is_staff:
            members = Members.objects.all()
            print(members)
            if request.method == "POST":
                if 'delete' == request.POST.get('status'):
                    id = request.POST.get('id')
                    try:
                        member_obj = Members.objects.get(id=id)
                        member_obj.delete()
                        return JsonResponse({'success':True})
                    except Exception as e:
                        print(e)
            return render(request, 'admin1/members_list.html', {'username':username, 'members':members})
        return HttpResponse("you are not admin to access this page")
    raise Http404("Page not found")

def admin_members_profile(request, id):
    authenticated = request.session.get('authenticated', False)
    username = request.session.get('username', None)
    if authenticated:
        if request.user.is_staff:
            member = get_object_or_404(Members, id=id)
            if member:
                return render(request, 'admin1/members_profile.html', {'member': member})
            return Http404("Member not found")
        return HttpResponse("You are not allowed to view this profile")
    return HttpResponse("You are not allowed to view this profile")

def admin_posts(request):
    authenticated = request.session.get('authenticated', False)
    username = request.session.get('username', None)
    if authenticated:
        if request.user.is_staff:
            search_query = request.GET.get('search', '')
            items = Post.objects.filter(title__icontains=search_query).order_by('-publication_date')  # Adjust the filter to your needs

            paginator = Paginator(items, 10)  # Show 10 items per page
            page_number = request.GET.get('page')
            page_obj = paginator.get_page(page_number)

            context = {
                'page_obj': page_obj,
                'search_query': search_query,
            }
            return render(request , 'admin1/posts.html', context)
        return HttpResponse("you are not allowed to access this page")
    return HttpResponse("you are not allowed to access this page")

def delete_post(request, id):
    authenticated = request.session.get('authenticated', False)
    username = request.session.get('username', None)
    if authenticated:
        if request.user.is_staff:
            obj = Post.objects.get(id=id)
            status = obj.delete()
            return redirect('admin_posts')
        return HttpResponse("you are not authenticated to this site")
    return HttpResponse("you are not authenticated to this site")

def delete_member(request, id):
    authenticated = request.session.get('authenticated', False)
    username = request.session.get('username', None)
    if authenticated:
        if request.user.is_staff:
            obj = Members.objects.get(id=id)
            status = obj.delete()
            return redirect('admin_members')
        return HttpResponse("you are not authenticated to this site")
    return HttpResponse("you are not authenticated to this site")


def edit_post(request, pk):
    authenticated = request.session.get('authenticated', False)
    if authenticated:
        if request.user.is_staff:
            post = get_object_or_404(Post, pk=pk)
            if request.method == "POST":
                title = request.POST.get('title')
                content = request.POST.get('content')
                author_id = request.POST.get('author')
                category_id = request.POST.get('category')

                post.title = title
                post.content = content
                post.author = get_object_or_404(Members, pk=author_id)
                post.category = get_object_or_404(Category, pk=category_id)
                post.save()

                images = request.FILES.getlist('images')
                if images:
                    # Optionally clear existing images if required
                    Image.objects.filter(post=post).delete()
                    for image in images:
                        Image.objects.create(post=post, image=image)

                return redirect('/admin-posts/')

            authors = Members.objects.all()
            categories = Category.objects.all()
            return render(request, 'admin1/edit_post.html', {'post': post, 'authors': authors, 'categories': categories})
        return HttpResponse('You are not allowed to edit this post', status=403)
    return HttpResponse('You are not allowed to edit this post', status=403)

def add_post(request):
    authenticated = request.session.get('authenticated', False)
    if authenticated:
        if request.user.is_staff:
            if request.method == "POST":
                title = request.POST.get('title')
                content = request.POST.get('content')
                author =request.POST.get('author')
                category = request.POST.get('category')
                try:
                    image = request.FILES['image']
                except KeyError:
                    profile_image = None
                if title and content and author and category:
                    author = get_object_or_404(Members, id=author)
                    category = get_object_or_404(Category, id=category)
                    post = Post.objects.create(title=title, content=content, author=author, category=category)
                    if post and image:
                        img = Image.objects.create(post=post, image=image)
                        if img:
                            return redirect('/admin-posts/')
                else:
                    return render(request, 'admin1/add_post.html',{'error_message':'please enter a post title, content, author, image and category'})
            return render(request, 'admin1/add_post.html', {'authors': Members.objects.all(), 'categories': Category.objects.all()})
        return HttpResponse("you are not admin to access this page")
    raise Http404("Page not found")

def add_member(request):
    authenticated = request.session.get('authenticated', False)
    if authenticated:
        if request.user.is_staff:
            if request.method == "POST":
                first_name = request.POST.get('first_name')
                last_name = request.POST.get('last_name')
                role = request.POST.get('role')
                profession =request.POST.get('profession')
                email = request.POST.get('email')
                phone = request.POST.get('phone')
                location = request.POST.get('location')
                facebook_link = request.POST.get('facebook_link')
                instagram_link = request.POST.get('instagram_link')
                twitter_link = request.POST.get('twitter_link')
                linkedin_link = request.POST.get('linkedin_link')
                try:
                    profile_image = request.FILES['profile_image']
                except KeyError:
                    profile_image = None
                role = get_object_or_404(Role, pk=role)
                if first_name and last_name and email and phone and profile_image:
                    member = Members.objects.create(first_name=first_name, last_name=last_name, role=role, profession=profession, email=email, phone=phone, instagram_link=instagram_link, facebook_link=facebook_link, twitter_link=twitter_link, linkedin_link=linkedin_link, profile_image=profile_image, address=location)
                    if member:
                        return redirect('/admin-members/')
                else:
                    return render(request, 'admin1/add_member.html',{'error_message':'please enter all details'})
            return render(request, 'admin1/add_member.html', {'authors': Members.objects.all(), 'categories': Category.objects.all(), 'roles': Role.objects.all()})
        return HttpResponse("you are not admin to access this page")
    raise Http404("Page not found")



def post_detail(request, slug):
    category = Category.objects.all().order_by('-id')
    obj = get_object_or_404(Post, slug=slug)
    return render(request, 'post_detail.html', {'obj': obj, 'category': category, 'year': datetime.now().year,})



def edit_member(request, member_id):
    authenticated = request.session.get('authenticated', False)
    if authenticated:
        if request.user.is_staff:
            print("member_id", member_id)
            member = get_object_or_404(Members, id=member_id)
            print(member.email)
            if request.method == "POST":
                member.first_name = request.POST.get('first_name')
                member.last_name = request.POST.get('last_name')
                member.profession = request.POST.get('profession')
                member.email = request.POST.get('email')
                member.phone = request.POST.get('phone')
                member.address = request.POST.get('address')
                member.facebook_link = request.POST.get('facebook_link')
                member.instagram_link = request.POST.get('instagram_link')
                member.twitter_link = request.POST.get('twitter_link')
                member.linkedin_link = request.POST.get('linkedin_link')
                role_inp = request.POST.get('role')
                role = get_object_or_404(Role, id=role_inp)
                
                if role:
                    member.role = role
                if 'profile_image' in request.FILES:
                    member.profile_image = request.FILES['profile_image']

                member.save()
                return redirect(f'/admin-members/{member_id}')
            return render(request, 'admin1/edit_member.html', {'member': member, 'roles': Role.objects.all()})
        return HttpResponse("You are not authorized to edit this member", status=403)
    return HttpResponse("You are not authorized to edit this member", status=403)

def logout_view(request):
    logout(request)
    return redirect('index')

def team(request):
    members = Members.objects.all().order_by('first_name')
    category = Category.objects.all().order_by('-id')

    return render(request, 'team.html', {'members':members, 'category':category, 'year':datetime.now().year})

def team_profile(request, pk):
    member = Members.objects.get(id=pk)
    category = Category.objects.all().order_by('-id')

    return render(request, 'team_profile.html', {'member':member, 'category':category, 'year':datetime.now().year})


def about(request):
    category = Category.objects.all().order_by('-id')
    return render(request, 'about.html', { 'category':category, 'year':datetime.now().year})

def donate(request):
    category = Category.objects.all().order_by('-id')
    return render(request, 'donate.html', { 'category':category, 'year':datetime.now().year})

def category(request):
    type = request.GET.get('type')
    items = Post.objects.filter(category__type__icontains=type).order_by('-publication_date')  # Adjust the filter to your needs
    paginator = Paginator(items, 10)  # Show 10 items per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    category = Category.objects.all().order_by('-id')
    posts =  Post.objects.all().order_by('-publication_date')
    context = {
        'page_obj': page_obj,
        'category': category,
        'type': type,
        'posts': posts,
        'year': datetime.now().year,
    }

    return render(request, 'category.html', context)

def submit_article(request):
    category = Category.objects.all().order_by('-id')
    return render(request, 'submit_article.html', {'category':category, 'year':datetime.now().year})

