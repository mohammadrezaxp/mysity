from django.contrib.sitemaps import Sitemap
from django.urls import reverse

from blog.visibility import public_posts


class BlogSitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.5

    def items(self):
        return public_posts()

    def lastmod(self, obj):
        return obj.published_date

    def get_absolute_url(self, obj):
        return reverse("blog:blog_single", kwargs={"name": obj.id})
