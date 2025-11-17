from django.contrib import admin
from django_summernote.admin import SummernoteModelAdmin

from blogapp.models import Blog, Comment

admin.site.register(Comment)

class CommentInline(admin.TabularInline):
    model = Comment
    fields = ['content', 'author']
    extra = 1

# Register your models here.
@admin.register(Blog)
class BlogAdmin(SummernoteModelAdmin):
  summernote_fieldsets = ['content',]
  inlines = [CommentInline]

