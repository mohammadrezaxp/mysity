from django.test import TestCase
from django.contrib.auth.models import User
from rest_framework.test import APIClient
from blog.models import Post, Category, Comments

class BlogModelTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='password123')
        self.category = Category.objects.create(name='Tech')

    def test_post_creation(self):
        post = Post.objects.create(
            auther=self.user,
            title='Test Post',
            content='Test Content',
            status=True
        )
        post.category.add(self.category)
        self.assertEqual(str(post), 'Test Post')
        self.assertTrue(post.status)
        self.assertEqual(post.count_comment(), 0)

    def test_comment_creation(self):
        post = Post.objects.create(
            auther=self.user,
            title='Test Post',
            content='Test Content',
            status=True
        )
        comment = Comments.objects.create(
            post=post,
            name='Visitor',
            subject='Nice',
            message='Great post!',
            email='visitor@example.com'
        )
        self.assertEqual(str(comment).startswith('Visitor'), True)
        self.assertEqual(post.count_comment(), 1)


class BlogApiTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='apiuser', password='password123')
        self.category = Category.objects.create(name='Python')
        self.post = Post.objects.create(
            auther=self.user,
            title='API Post',
            content='API Content',
            status=True
        )
        self.post.category.add(self.category)

    def test_get_posts_list(self):
        response = self.client.get('/api/posts/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()['results']), 1)

    def test_get_post_detail(self):
        response = self.client.get(f'/api/posts/{self.post.id}/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['title'], 'API Post')

    def test_jwt_token_obtain(self):
        response = self.client.post('/api/token/', {'username': 'apiuser', 'password': 'password123'})
        self.assertEqual(response.status_code, 200)
        self.assertIn('access', response.json())
