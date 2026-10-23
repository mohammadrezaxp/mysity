from datetime import timedelta
from io import BytesIO
from unittest.mock import patch

import pytest
from django.contrib.auth.models import User
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import Client
from django.urls import reverse
from django.utils import timezone
from PIL import Image
from rest_framework.test import APIClient

from blog.models import Category, Comments, Post

pytestmark = pytest.mark.django_db


@pytest.fixture
def content():
    owner = User.objects.create_user(
        "owner", email="owner@example.org", password="SecurePass!987"
    )
    other = User.objects.create_user(
        "other", email="other@example.org", password="SecurePass!987"
    )
    staff = User.objects.create_user(
        "editor", email="editor@example.org", password="SecurePass!987", is_staff=True
    )
    public = Post.objects.create(
        auther=owner,
        title="Public article",
        content="<p>Public content</p>",
        status=True,
    )
    draft = Post.objects.create(
        auther=owner, title="Draft article", content="Private draft", status=False
    )
    future = Post.objects.create(
        auther=owner,
        title="Future article",
        content="Scheduled content",
        status=True,
        published_date=timezone.now() + timedelta(days=7),
    )
    member = Post.objects.create(
        auther=owner,
        title="Members article",
        content="Members content",
        status=True,
        login_re=True,
    )
    return dict(
        owner=owner,
        other=other,
        staff=staff,
        public=public,
        draft=draft,
        future=future,
        member=member,
    )


def api(user=None):
    c = APIClient()
    if user:
        c.force_authenticate(user)
    return c


def test_post_author_cannot_be_spoofed_or_changed(content):
    c = api(content["other"])
    response = c.post(
        "/api/posts/",
        {
            "title": "My article",
            "content": "Text",
            "status": False,
            "auther": content["owner"].pk,
        },
        format="json",
    )
    assert response.status_code == 201
    post = Post.objects.get(pk=response.data["id"])
    assert post.auther == content["other"]
    response = c.patch(
        f"/api/posts/{post.pk}/", {"auther": content["owner"].pk}, format="json"
    )
    assert response.status_code == 200
    post.refresh_from_db()
    assert post.auther == content["other"]


def test_foreign_post_edits_denied(content):
    c = api(content["other"])
    post = content["public"]
    assert c.patch(f"/api/posts/{post.pk}/", {"title": "Stolen"}).status_code == 403
    assert c.delete(f"/api/posts/{post.pk}/").status_code == 403
    assert (
        api(content["staff"])
        .patch(f"/api/posts/{post.pk}/", {"title": "Edited"})
        .status_code
        == 200
    )


def test_category_writes_require_staff(content):
    c = api(content["other"])
    assert c.post("/api/categories/", {"name": "Untrusted"}).status_code == 403
    category = Category.objects.create(name="Technology")
    assert (
        c.patch(f"/api/categories/{category.pk}/", {"name": "Changed"}).status_code
        == 403
    )
    assert (
        api(content["staff"])
        .post("/api/categories/", {"name": "Editorial"})
        .status_code
        == 201
    )


def test_comment_owner_and_private_email(content):
    c = api(content["other"])
    response = c.post(
        "/api/comments/",
        {
            "post": content["public"].pk,
            "subject": "Feedback",
            "message": "Helpful article",
            "email": "private@example.org",
        },
        format="json",
    )
    assert response.status_code == 201
    comment = Comments.objects.get(pk=response.data["id"])
    assert comment.author == content["other"]
    assert "email" not in response.data
    assert "email" not in api().get(f"/api/comments/{comment.pk}/").data
    assert (
        api(content["owner"])
        .patch(f"/api/comments/{comment.pk}/", {"message": "Hijacked"})
        .status_code
        == 403
    )
    assert (
        c.patch(f"/api/comments/{comment.pk}/", {"message": "Updated"}).status_code
        == 200
    )
    assert (
        api(content["staff"]).delete(f"/api/comments/{comment.pk}/").status_code == 204
    )


def test_legacy_unowned_comment_is_staff_managed(content):
    comment = Comments.objects.create(
        post=content["public"],
        name="Legacy",
        email="legacy@example.org",
        subject="Old",
        message="Historical comment",
    )
    assert (
        api(content["other"])
        .patch(f"/api/comments/{comment.pk}/", {"message": "tampered"})
        .status_code
        == 403
    )
    assert (
        api(content["staff"])
        .patch(f"/api/comments/{comment.pk}/", {"message": "Moderated"})
        .status_code
        == 200
    )


def test_comments_cannot_leak_drafts_or_future_posts(content):
    for name in ["draft", "future", "member"]:
        comment = Comments.objects.create(
            post=content[name],
            name="Hidden",
            email="hidden@example.org",
            subject="Hidden",
            message="Hidden feedback",
        )
        assert api().get(f"/api/comments/{comment.pk}/").status_code == 404
        if name != "member":
            assert (
                api(content["other"])
                .post(
                    "/api/comments/",
                    {
                        "post": content[name].pk,
                        "subject": "Attack",
                        "message": "Attack",
                    },
                )
                .status_code
                == 400
            )


@pytest.mark.parametrize("name", ["draft", "future", "member"])
def test_anonymous_post_detail_rejects_nonpublic_content(content, name):
    assert api().get(f"/api/posts/{content[name].pk}/").status_code == 404


def test_author_preview_and_authenticated_member_visibility(content):
    for name in ["draft", "future", "member"]:
        assert (
            api(content["owner"]).get(f"/api/posts/{content[name].pk}/").status_code
            == 200
        )
    assert (
        api(content["other"]).get(f"/api/posts/{content['member'].pk}/").status_code
        == 200
    )


def test_future_publication_does_not_leak_from_discovery(client, content):
    category = Category.objects.create(name="Hidden category")
    content["future"].category.add(category)
    content["future"].tag.add("scheduled")
    paths = [
        "/api/posts/",
        "/blog/",
        "/blog/search/?search=Scheduled",
        "/blog/category/Hidden%20category/",
        "/blog/tag/scheduled/",
        "/ref/home/",
        "/blog/rss/feed/",
        "/ref/sitemap.xml",
    ]
    for path in paths:
        response = client.get(path)
        assert response.status_code == 200, path
        assert b"Future article" not in response.content, path
        assert b"Private draft" not in response.content, path
        if path.endswith("sitemap.xml"):
            assert f'/blog/{content["future"].pk}/'.encode() not in response.content


def test_public_detail_is_public_and_view_counter_increments(client, content):
    post = content["public"]
    before = post.counted_views
    response = client.get(f"/blog/{post.pk}/")
    assert response.status_code == 200
    post.refresh_from_db()
    assert post.counted_views == before + 1


def test_tag_filter_uses_actual_model_field(client, content):
    content["public"].tag.add("python")
    response = client.get("/blog/tag/python/")
    assert response.status_code == 200
    assert b"Public article" in response.content


def test_rich_html_is_sanitized_on_input_and_legacy_output(client, content):
    post = content["public"]
    payload = '<p style="color:red">Keep this</p><script>alert(1)</script><img src="x" onerror="alert(1)"><a href="javascript:alert(1)">Click</a>'
    response = api(content["owner"]).patch(
        f"/api/posts/{post.pk}/", {"content": payload}
    )
    assert response.status_code == 200
    assert "<script" not in response.data["content"]
    assert "onerror" not in response.data["content"]
    assert "javascript:" not in response.data["content"]
    assert "<p" in response.data["content"]
    Post.objects.filter(pk=post.pk).update(content=payload)
    response = client.get(f"/blog/{post.pk}/")
    assert b"<script>alert(1)</script>" not in response.content
    assert b'onerror="alert(1)"' not in response.content


def test_tags_and_categories_roundtrip(content):
    category = Category.objects.create(name="Python")
    c = api(content["owner"])
    response = c.post(
        "/api/posts/",
        {
            "title": "Tagged",
            "content": "Text",
            "status": True,
            "tag": ["python", "django"],
            "category_ids": [category.pk],
        },
        format="json",
    )
    assert response.status_code == 201
    assert set(response.data["tag"]) == {"python", "django"}
    assert response.data["category"][0]["id"] == category.pk
    response = c.patch(
        f"/api/posts/{response.data['id']}/", {"tag": ["updated"]}, format="json"
    )
    assert response.status_code == 200
    assert response.data["tag"] == ["updated"]


def test_counter_and_timestamps_are_read_only(content):
    post = content["public"]
    response = api(content["owner"]).patch(
        f"/api/posts/{post.pk}/", {"counted_views": 99999}
    )
    assert response.status_code == 200
    post.refresh_from_db()
    assert post.counted_views == 0


def test_login_external_redirect_rejected(client, content):
    response = client.post(
        reverse("User_manage:login"),
        {
            "username": "owner",
            "password": "SecurePass!987",
            "next": "https://example.org/steal",
        },
    )
    assert response.status_code == 302
    assert response.url == reverse("index")


def test_logout_requires_post_and_csrf(content):
    c = Client(enforce_csrf_checks=True)
    c.force_login(content["owner"])
    assert c.get(reverse("User_manage:logout")).status_code == 405
    assert c.post(reverse("User_manage:logout")).status_code == 403


def test_registration_validates_email_and_password(client):
    for data in [
        dict(
            username="new",
            email="invalid",
            password="StrongEnough!978",
            password_confirm="StrongEnough!978",
        ),
        dict(
            username="new",
            email="new@example.org",
            password="123456",
            password_confirm="123456",
        ),
    ]:
        assert client.post(reverse("User_manage:sing_up"), data).status_code == 200
        assert not User.objects.filter(username="new").exists()
    response = client.post(
        reverse("User_manage:sing_up"),
        dict(
            username="new",
            email="NEW@example.org",
            password="StrongEnough!978",
            password_confirm="StrongEnough!978",
        ),
    )
    assert response.status_code == 302
    assert User.objects.get(username="new").check_password("StrongEnough!978")


def test_browser_comment_uses_authenticated_identity_and_rejects_hidden_post(
    client, content
):
    client.force_login(content["other"])
    data = dict(
        post_id=content["public"].pk,
        name="Forged admin",
        email="fake@example.org",
        subject="Feedback",
        message="Real author",
    )
    response = client.post(reverse("blog:blog_comment"), data)
    assert response.status_code == 302
    comment = Comments.objects.get(message="Real author")
    assert comment.author == content["other"]
    assert comment.name == "other"
    assert comment.email == "other@example.org"
    data["post_id"] = content["draft"].pk
    assert client.post(reverse("blog:blog_comment"), data).status_code == 404


def test_contact_preserves_submitted_name(client):
    from mysity.models import Contact

    with patch("captcha.fields.CaptchaField.clean", return_value="passed"):
        response = client.post(
            reverse("contact"),
            dict(
                name="Real visitor",
                email="visitor@example.org",
                subject="Hello",
                message="A question",
                captcha_0="key",
                captcha_1="ok",
            ),
        )
    assert response.status_code == 302
    assert Contact.objects.get().name == "Real visitor"


def test_editor_upload_rejects_anonymous_and_nonstaff(client, content):
    url = reverse("django_summernote-upload_attachment")
    assert client.post(url, {}).status_code in (302, 403)
    client.force_login(content["other"])
    assert client.post(url, {}).status_code == 403


def test_staff_editor_image_upload(client, content, tmp_path, settings):
    settings.MEDIA_ROOT = tmp_path
    client.force_login(content["staff"])
    file = BytesIO()
    Image.new("RGB", (10, 10), "blue").save(file, format="PNG")
    upload = SimpleUploadedFile("editor.png", file.getvalue(), content_type="image/png")
    response = client.post(
        reverse("django_summernote-upload_attachment"), {"files": upload}
    )
    assert response.status_code == 200


def test_schema_and_auth_canonical_routes(client):
    assert reverse("User_manage:login") == "/ref/user_manage/login/"
    assert client.get("/api/schema/").status_code == 200
    assert client.get("/ref/user_manage/login/").status_code == 200
