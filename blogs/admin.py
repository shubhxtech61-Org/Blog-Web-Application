from turtle import title
from django.contrib import admin
from .models import Blog, Comment, category

# for auto genrate slugs
class BlogAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('title',)}
    list_display = ('title', 'category', 'author', 'status', 'is_featured')
    search_fields = ('id', 'title', 'category__category_name', 'status')
    list_editable = ('is_featured', )

# Register your models here.
admin.site.register(category)
admin.site.register(Blog, BlogAdmin)
admin.site.register(Comment)