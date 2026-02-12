from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from .models import Video

# Create your views here.
def home_view(request):
    return render(request, "main/home.html")

@login_required
def profile_view(request):
    videos = Video.objects.filter(user=request.user).order_by("-uploaded_at")

    return render(request, "main/profile.html", {
        "videos": videos
    })

@login_required
def upload_view(request):
    if request.method == "POST":
        video_file = request.FILES.get("video")

        if video_file:
            Video.objects.create(
                user=request.user,
                title="Test",
                video=video_file
            )
            return redirect("home")
    return render(request, "main/upload.html")

def logout_view(request):
    logout(request)
    return redirect("home")

def login_view(request):
    if request.method == "POST":
        user = authenticate(
            request,
            username=request.POST.get("username"),
            password=request.POST.get("password"),
        )
        if user:
            login(request, user)
            return redirect("home")

    return render(request, "main/login.html")


def signup_view(request):
    if request.method == "POST":
        user = User.objects.create_user(
            username=request.POST.get("username"),
            email=request.POST.get("email"),
            password=request.POST.get("password"),
        )
        login(request, user)
        return redirect("home")

    return render(request, "main/signup.html")
