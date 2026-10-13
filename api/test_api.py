import pytest
from django.urls import reverse
from rest_framework import status

@pytest.mark.django_db
def test_post_list(client):
    url = reverse('post-list')
    response = client.get(url)
    assert response.status_code == status.HTTP_200_OK

@pytest.mark.django_db
def test_token_obtain(client):
    url = reverse('token_obtain_pair')
    response = client.post(url, {'username': 'testuser', 'password': 'testpassword'})
    # Expect 401 as user doesn't exist yet
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
