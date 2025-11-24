from django.contrib import admin
from blog.models import Post , Category , Comments
from  django_summernote.admin import SummernoteModelAdmin
@admin.register(Post)
class PostAdmin(SummernoteModelAdmin):
    date_hierarchy = 'created_date'
    empty_value_display = '-empty-'
   # fields = ('title',)
    list_display = ('title','auther','counted_views','status','published_date','created_date')
    list_filter = ('status',)
   # ordering = ['created_date']
    search_fields = ['title','content']
    summernote_fields = ('content',)
    # admin.sit.register(Post)
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    pass

@admin.register(Comments)
class CommentAdmin(admin.ModelAdmin):
    pass