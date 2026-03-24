from django.contrib.auth.models import User
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase
from django.urls import reverse

from .models import Video


class AuthViewTests(TestCase):
    def test_signup_creates_user_and_logs_them_in(self):
        response = self.client.post(
            reverse("signup"),
            {
                "username": "rahim",
                "email": "rahim@gmail.com",
                "password": "test-pass-123",
            },
        )

        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json()["message"], "signup successful")
        self.assertTrue(User.objects.filter(username="rahim").exists())
        self.assertEqual(int(self.client.session["_auth_user_id"]), User.objects.get(username="rahim").id)

    def test_login_rejects_invalid_credentials(self):
        User.objects.create_user(username="rahim", password="correct-password")

        response = self.client.post(
            reverse("login"),
            {"username": "rahim", "password": "wrong-password"},
        )

        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.json()["error"], "invalid credentials")

    def test_login_accepts_valid_credentials(self):
        user = User.objects.create_user(username="rahim", password="correct-password")

        response = self.client.post(
            reverse("login"),
            {"username": "rahim", "password": "correct-password"},
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["message"], "login successful")
        self.assertEqual(int(self.client.session["_auth_user_id"]), user.id)


class VideoViewTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="karim", password="test-pass-123")
        self.other_user = User.objects.create_user(username="farhan", password="test-pass-123")

    def test_videos_endpoint_requires_authentication(self):
        response = self.client.get(reverse("videos"))

        self.assertEqual(response.status_code, 302)

    def test_videos_endpoint_returns_only_logged_in_users_videos(self):
        self.client.force_login(self.user)

        own_video = Video.objects.create(
            user=self.user,
            title="my video",
            video=SimpleUploadedFile("mine.mp4", b"video-content", content_type="video/mp4"),
        )
        Video.objects.create(
            user=self.other_user,
            title="other video",
            video=SimpleUploadedFile("other.mp4", b"video-content", content_type="video/mp4"),
        )

        response = self.client.get(reverse("videos"))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), [
            {
                "id": own_video.id,
                "title": "my video",
                "video_url": own_video.video.url,
                "uploaded_at": own_video.uploaded_at.isoformat(),
            }
        ])

    def test_video_detail_returns_metadata(self):
        self.client.force_login(self.user)
        video = Video.objects.create(
            user=self.other_user,
            title="shared video",
            video=SimpleUploadedFile("shared.mp4", b"video-content", content_type="video/mp4"),
        )

        response = self.client.get(reverse("video-detail", args=[video.id]))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.json(),
            {
                "id": video.id,
                "title": "shared video",
                "video_url": video.video.url,
                "uploaded_by": self.other_user.username,
                "uploaded_at": video.uploaded_at.isoformat(),
            },
        )

    def test_upload_video_api_rejects_missing_file(self):
        self.client.force_login(self.user)

        response = self.client.post(reverse("video-upload-api"))

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json()["error"], "No video file provided")

    def test_upload_video_api_creates_video_record(self):
        self.client.force_login(self.user)

        response = self.client.post(
            reverse("video-upload-api"),
            {
                "video": SimpleUploadedFile(
                    "clip.mp4",
                    b"video-content",
                    content_type="video/mp4",
                )
            },
        )

        self.assertEqual(response.status_code, 201)
        created = Video.objects.get(user=self.user)
        self.assertEqual(created.title, "clip")
        self.assertEqual(response.json()["id"], created.id)
