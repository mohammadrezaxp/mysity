from django.contrib.syndication.views import Feed
from django.template.defaultfilters import truncatewords
from django.utils.html import strip_tags

from blog.visibility import public_posts


class LatestEntriesFeed(Feed):
    title = "best blog news"
    link = "/rss/feed"
    description = "You can see best blog "

    def items(self):
        return public_posts()

    def item_title(self, item):
        return item.title

    def item_description(self, item):
        plain_text = strip_tags(item.content)
        return truncatewords(plain_text, 50)
