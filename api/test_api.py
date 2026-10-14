import pytest
from django.urls import reverse
from rest_framework import status
from django.contrib.auth.models import User
from blog.models import Post, Category, Comments

@pytest.mark.django_db
def test_post_list(client):
    url = reverse('post-list')
    response = client.get(url)
    assert response.status_code == status.HTTP_200_OK

@pytest.mark.django_db
def test_category_list(client):
    url = reverse('category-list')
    response = client.get(url)
    assert response.status_code == status.HTTP_200_OK

@pytest.mark.django_db
def test_comment_list(client):
    url = reverse('comments-list')
    response = client.get(url)
    assert response.status_code == status.HTTP_200_OK

@pytest.mark.django_db
def test_token_obtain_unauthorized(client):
    url = reverse('token_obtain_pair')
    response = client.post(url, {'username': 'nonexistent', 'password': 'wrongpassword'})
    assert response.status_code == status.HTTP_401_UNAUTHORIZED

@pytest.mark.django_db
def test_token_lifecycle():
    from rest_framework_simplejwt.tokens import RefreshToken
    user = User.objects.create_user(username='authtest', password='password123')
    refresh = RefreshToken.for_user(user)
    access = str(refresh.access_token)
    assert access is not None
    assert str(refresh) is not None

@pytest.mark.django_db
def test_draft_post_visibility(client):
    user = User.objects.create_user(username='author1', password='password123')
    public_post = Post.objects.create(title='Public Post', content='Content', status=True, auther=user)
    draft_post = Post.objects.create(title='Draft Post', content='Content', status=False, auther=user)
    
    url = reverse('post-list')
    response = client.get(url)
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    titles = [p['title'] for p in (data.get('results', data) if isinstance(data, dict) else data)]
    assert 'Public Post' in titles
    assert 'Draft Post' not in titles

