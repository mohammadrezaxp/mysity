from django.contrib import admin
from mysity.models import Contact , news
@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    date_hierarchy = 'created_date'
    fields = ('name','subject','email','message')
    list_display = ('name','subject','created_date')
    list_filter = ('email',)
    search_fields = ('name','subject')

@admin.register(news)
class newsAdmin(admin.ModelAdmin):
    fields = ('email',)


