from django.shortcuts import render,get_object_or_404
from .models import Post,Comment
from django.core.paginator import Paginator,EmptyPage,PageNotAnInteger
from django.views.generic import ListView
from .forms import EmailPostForm,CommentForm
from django.core.mail import send_mail
from taggit.models import Tag
from django.db.models import Count

# Create your views here.
#first
#def post_list(request):
#	object_list = Post.published.all()
#	paginator = Paginator(object_list,3)
#	page = request.GET.get('page')
#	try:
#		posts = paginator.page(page)
#	except PageNotAnInteger: # first page when pagenumber doesnot exist
#		posts = paginator.page(1)
#	except EmptyPage:
#		#if page is out of rang
#		posts = paginator.page(Paginator.num_pages)
#	template = 'blog/post/list.html'
#	return render(request,template,{'posts':posts,'page':page})

#def post_detail(request,year,month,day,post):
#	post = get_object_or_404(Post, slug=post, status='published', publish__year=year, publish__month=month,publish__day=day)
#	template = 'blog/post/detail.html'
#	return render(request,template,{'post':post})

#class PostListView(ListView):
#	queryset = Post.published.all()
#	context_object_name = 'posts'
#	template_name = 'blog/post/list.html'
#	paginate_by = 3

def post_list(request,tag_slug=None):
	object_list = Post.published.all()
	tag = None

	if tag_slug:
		tag = get_object_or_404(Tag,slug=tag_slug)
		object_list = object_list.filter(tags__in=[tag])
	paginator = Paginator(object_list,3)
	page = request.GET.get('page')
	try:
		posts = paginator.page(page)
	except PageNotAnInteger: # first page when pagenumber doesnot exist
		posts = paginator.page(1)
	except EmptyPage:
		#if page is out of rang
		posts = paginator.page(Paginator.num_pages)
	template = 'blog/post/list.html'
	return render(request,template,{'posts':posts,'page':page,'tag':tag})

def post_share(request,post_id):
	#retrieve post by id
	post = get_object_or_404(Post,id=post_id,status='published')
	sent = False

	if request.method == 'POST':
		#form was submitted
		form = EmailPostForm(request.POST)
		if form.is_valid():
			#form field passed validation
			cd = form.cleaned_data
			post_url = request.build_absolute_uri(post.get_absolute_url())
			subject = '{}({}) recommends you reading {}'.format(cd['name'],cd['email'],post.title)
			message = 'Read {} at {}\n\n{}\'s comments:{}'.format(post.title,post_url,cd['name'],cd['comments'])
			send_mail(subject,message,'shahzan@myblog.com',[cd['to']])
			sent = True
	else:
		form = EmailPostForm()
	return render(request,'blog/post/share.html',{'post':post,'form':form,'sent':sent})

def post_detail(request,year,month,day,post):
	post = get_object_or_404(Post, slug=post, status='published', publish__year=year, publish__month=month,publish__day=day)

	#list of active comments for this post
	comments = post.comments.filter(active=True)
	new_comment = None
	if request.method == 'POST':
		#a comment is being posted
		comment_form = CommentForm(data = request.POST)
		if comment_form.is_valid():
			#create a comment object but dont save it yet
			new_comment = comment_form.save(commit=False)
			#assign the current post to the comment
			new_comment.post = post
			#save the new comment to database
			new_comment.save()
	else:
		comment_form = CommentForm()
	template = 'blog/post/detail.html'
	#list of similar posts
	post_tags_ids = post.tags.values_list('id',flat=True)
	similar_posts = Post.published.filter(tags__in=post_tags_ids).exclude(id=post.id)
	similar_posts = similar_posts.annotate(same_tags=Count('tags')).order_by('-same_tags','-publish')[:4]
	return render(request,template,{'post':post,'new_comment':new_comment,'comment_form':comment_form,'comments':comments,'similar_posts':similar_posts})
