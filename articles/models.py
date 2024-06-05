from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify
from django.db.models.signals import pre_save


class Role(models.Model):
    type = models.CharField(max_length=255)

    def __str__(self):
        return self.type

class Members(models.Model):
    first_name = models.CharField(max_length=40)
    last_name = models.CharField(max_length=40)
    email = models.EmailField()
    phone = models.CharField(max_length=10)
    role = models.ForeignKey(Role, on_delete=models.CASCADE, default=3)
    profession = models.TextField(blank=True)
    address = models.TextField(blank=True)
    profile_image = models.ImageField(upload_to='post_members/')
    instagram_link = models.TextField(blank=True)
    twitter_link = models.TextField(blank=True)
    facebook_link = models.TextField(blank=True)
    linkedin_link = models.TextField(blank=True)

    def __str__(self):
        return self.first_name + " " + self.last_name

class Category(models.Model):
    type = models.CharField(max_length=255)

    def __str__(self):
        return self.type

class Post(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    author = models.ForeignKey(Members, on_delete=models.CASCADE)
    publication_date = models.DateTimeField(auto_now_add=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, default=1)
    slug = models.SlugField(unique=True, max_length=255, default=None)

    def __str__(self):
        return self.title

def create_slug(instance, new_slug=None):
    slug = slugify(instance.title) if new_slug is None else new_slug
    qs = Post.objects.filter(slug=slug).order_by('-id')
    if qs.exists():
        new_slug = f"{slug}-{qs.first().id}"
        return create_slug(instance, new_slug=new_slug)
    return slug

def pre_save_post_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = create_slug(instance)

pre_save.connect(pre_save_post_receiver, sender=Post)


class Image(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='post_images/')

    def __str__(self):
        return f"Image for {self.post.title}"

