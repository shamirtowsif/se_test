from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from .models import Video
import os
from django.http import JsonResponse
from django.shortcuts import get_object_or_404

@login_required
def videos_view(request):
    videos = Video.objects.filter(user=request.user).order_by("-uploaded_at")

    data = []

    for video in videos:
        data.append({
            "id": video.id,
            "title": video.title,
            "video_url": video.video.url,
            "uploaded_at": video.uploaded_at.isoformat(),
        })

    return JsonResponse(data, safe=False)

@login_required
def video_detail(request, video_id):
    video = get_object_or_404(Video, id=video_id)

    return JsonResponse({
        "id": video.id,
        "title": video.title,
        "video_url": video.video.url,
        "uploaded_by": video.user.username,
        "uploaded_at": video.uploaded_at.isoformat(),
    })

@login_required
def upload_video_api(request):
    if request.method == "POST":
        video_file = request.FILES.get("video")

        if not video_file:
            return JsonResponse({"error": "No video file provided"}, status=400)

        filename = os.path.splitext(video_file.name)[0]

        video = Video.objects.create(
            user=request.user,
            title=filename,
            video=video_file
        )

        return JsonResponse({
            "message": "Video uploaded successfully",
            "id": video.id,
            "title": video.title,
            "video_url": video.video.url,
            "uploaded_at": video.uploaded_at.isoformat(),
        }, status=201)

    return JsonResponse({"error": "Invalid request method"}, status=405)

# Create your views here.
def home_view(request):
    return render(request, "main/home.html")


@login_required
def show_video_view(request, video_id):
    video = Video.objects.get(id=video_id)

    return render(request, "main/show_video.html", {
        "video": video
    })


@login_required
def profile_view(request):
    # videos = Video.objects.filter(user=request.user).order_by("-uploaded_at")

    return render(request, "main/profile.html")

@login_required
def upload_view(request):
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
