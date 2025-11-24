from django.contrib.sitemaps import Sitemap
from blog.models import Post
from django.urls import reverse
class BlogSitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.5

    def items(self):
        return Post.objects.filter(status=True)

    def lastmod(self, obj):
        return obj.published_date

    def get_absolute_url(self,obj):
        return reverse('blog:blog_single', kwargs={'name': obj.id})