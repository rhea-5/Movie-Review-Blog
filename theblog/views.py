from django.shortcuts import render,redirect
from .models import Post
from django.views import generic
#List a query set into the data base, and bring back record set
#Listview to send all blogs to db, detailview to fetch any one blog
from django.http import HttpResponse
from django.http import Http404
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from .forms import PostForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.validators import EmailValidator
from django.core.exceptions import ValidationError
import re


 # Create your views here.
def theblog(request):
     return render(request,'home.html')



class PostList(generic.ListView):
     queryset=Post.objects.filter(status=1).order_by('-created_on')
     template_name='home.html'

class DetailView(generic.DetailView):
     model=Posttemplate_name='post_detail.html'



def login_page(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        if not User.objects.filter(username=username).exists():
            messages.error(request, 'invalid username')

        user = authenticate(request, username=username, password=password)

        if user is None:
            messages.error(request, 'invalid password')
            return redirect('/login/')
        
        else:
            login(request, user)
            return redirect('/home/')

    return render(request, 'login.html')

def logout_page(request):
    logout(request)
    return redirect('/login/')





def register(request):
    if request.method == "POST":
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        password_confirm = request.POST.get('password_confirm')

        email_validator = EmailValidator()
        try:
            email_validator(email)
        except ValidationError:
            messages.error(request, "Invalid email format.")
            return redirect('/signup/')

        # Check if the passwords match
        if password != password_confirm:
            messages.error(request, "Password and password confirmation do not match.")
            return redirect('/signup/')

        # Password validation
        if len(password) < 8 or not re.search(r'\d', password):
            messages.error(request, "Password must be at least 8 characters long and contain at least one digit.")
            return redirect('/signup/')

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists.")
            return redirect('/login/')

        user = User.objects.create_user(username=username, email=email, password=password)
        user.save()

        messages.info(request, "Account created successfully.")
        return redirect('/home/')
    

    return render(request, 'signup.html')

def signup(request):
     return render(request, 'signup.html')


@login_required
def create_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user  # Set the post author to the current user
            post.save()
            return redirect('home')
    else:
        form = PostForm()
    return render(request, 'create_post.html', {'form': form})

@login_required

def update_post(request, post_id):
    try:
        post = Post.objects.get(id=post_id)
    except Post.DoesNotExist:
        raise Http404("Post does not exist")

    if request.method == 'POST':
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            form.save()
            return redirect('/home/', post_id=post_id)
    else:
        form = PostForm(instance=post)

    return render(request, 'update_post.html', {'form': form})

@login_required
def delete_post(request, post_id):
    try:
        post = Post.objects.get(id=post_id)
    except Post.DoesNotExist:
        raise Http404("Post does not exist")

    if request.method == 'POST':
        post.delete()
        return redirect('/home/')  # Redirect to the home page after deleting the post

    return render(request, 'delete_post.html', {'post': post})

