from django.contrib.syndication.views import Feed
from django.urls import reverse
from django.utils.html import strip_tags
from django.template.defaultfilters import truncatewords
from .models import Post


class LatestEntriesFeed(Feed):
    title = "best blog news"
    link = "/rss/feed"
    description = "You can see best blog "

    def items(self):
        return Post.objects.filter(status=True)

    def item_title(self, item):
        return item.title

    def item_description(self, item):
        plain_text = strip_tags(item.content)
        return truncatewords(plain_text, 50)