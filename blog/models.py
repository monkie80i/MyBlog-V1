from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.urls import reverse
from taggit.managers import TaggableManager


# Create your models here.
#managers
class PublishedManager(models.Manager):
	def get_queryset(self):
		return super(PublishedManager,self).get_queryset().filter(status='published')

class DraftedManager(models.Manager):
	def get_queryset(self):
		return super(DraftedManager,self).get_queryset().filter(status='drafted')

class Post(models.Model):
	STATUS_CHOICES = (('drafted','Drafted'),('published','Published'))
	image = models.ImageField(upload_to='post/%Y/%m/%d/',blank=True)
	title = models.CharField(max_length=250)
	slug = models.SlugField(unique_for_date='publish')
	body = models.TextField()
	author = models.ForeignKey(User,related_name='blog_post',on_delete=models.CASCADE)
	publish = models.DateTimeField(default=timezone.now)
	created = models.DateTimeField(auto_now_add=True)
	updated = models.DateTimeField(auto_now=True)
	status = models.CharField(max_length=10,choices=STATUS_CHOICES,default='Drafted')
	objects = models.Manager()
	published = PublishedManager()
	drafted = DraftedManager()
	tags = TaggableManager()

	def get_absolute_url(self):
		return reverse('blog:post_detail',args=[self.publish.year,self.publish.month,self.publish.day,self.slug])

	class Meta:
		ordering = ('-publish',)

	def __str__(self):
		return self.title

class Comment(models.Model):
	post = models.ForeignKey(Post,related_name='comments',on_delete=models.CASCADE)
	#defautl_user = User.objects.get(username='admin')
	user = models.ForeignKey(User,related_name='comments',on_delete=models.CASCADE)
	body = models.TextField()
	created = models.DateTimeField(auto_now_add=True)
	updated = models.DateTimeField(auto_now=True)
	active = models.BooleanField(default=True)

	class Meta:
		ordering = ('-created',)
	
	def __str__(self):
		return "Comment by {} on {}".format(self.user.username,self.post)