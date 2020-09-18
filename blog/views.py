from django.shortcuts import render,get_object_or_404
from .models import Post,Comment
from django.core.paginator import Paginator,EmptyPage,PageNotAnInteger
from .forms import EmailPostForm,CommentForm
from django.core.mail import send_mail
from taggit.models import Tag
from django.db.models import Count
from django.conf import settings


# Create your views here.
def post_list(request,tag_slug=None):
	object_list = Post.published.all()
	tag = None
	page_name = 'home'

	if tag_slug:
		page_name = 'tag_list' 
		tag = get_object_or_404(Tag,slug=tag_slug)
		object_list = object_list.filter(tags__in =[tag])

	paginator = Paginator(object_list,3)
	page = request.GET.get('page')
	try:
		posts = paginator.page(page)
	except PageNotAnInteger:
		#first call
		posts = paginator.page(1)
	except EmptyPage:
		#last page
		posts = paginator.page(paginator.num_pages)
	return render(request,'blog/post/list.html',{'posts':posts,'tag':tag,'page':page_name})


def post_detail(request,year,month,day,post):
	post = get_object_or_404(Post,slug=post,status='published',publish__year=year,publish__month=month,publish__day=day)
	comments = Comment.objects.filter(active=True).filter(post=post)
	new_comment = False
	comment_form = None

	if request.user.is_authenticated:
		if request.method == 'POST':
			comment_form = CommentForm(data=request.POST)
			if comment_form.is_valid():
				new_comment = comment_form.save(commit=False)
				new_comment.post = post
				new_comment.user = request.user
				new_comment.save()
		else:
			comment_form = CommentForm()
	#get similar posts by tags
	post_tag_ids = post.tags.values_list('id',flat=True)
	similar_posts = Post.published.filter(tags__in=post_tag_ids)
	similar_posts = similar_posts.annotate(same_tags = Count('tags')).order_by('-same_tags','-publish')[:4]
	return render(request,'blog/post/detail.html',{'post':post,'comments':comments,'new_comment':new_comment,'form':comment_form,'similar_posts':similar_posts})

def post_share(request,post_id):
	post =  get_object_or_404(Post,id=post_id)
	sent = False

	if request.method == 'POST':
		form = EmailPostForm(data=request.POST)
		if form.is_valid():
			cd = form.cleaned_data
			# send mail
			post_url = request.build_absolute_uri(post.get_absolute_url())
			subject = "{} would like you to check out his post:{}".format(cd['name'],post.title)
			body = "Read {} at {}\n\n Comments by {}:{}".format(post.title,post_url,cd['name'],cd['comments'])
			from_email = settings.EMAIL_HOST_USER
			send_mail(subject,body,from_email,[cd['to']],fail_silently=False)
			sent = True
	else:
		form = EmailPostForm()

	return render(request,'blog/post/share.html',{'post':post,'form':form,'sent':sent})