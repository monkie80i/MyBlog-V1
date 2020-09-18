from django.contrib import admin
from .models import Post,Comment

# Register your models here.
@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
	list_display = ('title','author','created','status')
	list_filter = ('author','created','publish','status','updated')
	search_fields = ('title','body','author')
	prepopulated_fields = {'slug':('title',)}
	raw_id_fields = ('author',)
	date_hierarchy = 'publish'
	ordering = ('-publish','status')

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
	list_display = ('user','post','active')
	list_filter = ('created','post','active')
	search_fields = ('body',)
	ordering = ('-created',)