from django import template
from ..models import Post

register = template.Library()

@register.simple_tag
def total_posts():
	return Post.published.count()

@register.inclusion_tag('blog/post/latest.html')
def latest_posts(count=4):
	posts = Post.published.order_by('-publish')[:count]
	return {'latest_posts':posts}