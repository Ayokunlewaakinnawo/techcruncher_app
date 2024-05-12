from django.db import models
from django.utils.text import slugify
#from datetime import datetime

class NewsPost(models.Model):
    title = models.TextField(max_length=255)
    desc = models.TextField()
    url = models.CharField(max_length=255)
    slug = models.SlugField(unique=True, blank=True)
    author = models.TextField(max_length=255)
    body = models.TextField()
    image1 = models.ImageField(upload_to='images/', blank=True)
    image2 = models.ImageField(upload_to='images/', blank=True)
    date_added = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-date_added']#<---- Ordering from newest to oldest

    def save(self, *args, **kwargs):
        # Check for existing duplicates based on title and url
        duplicates = NewsPost.objects.filter(title=self.title, url=self.url).exclude(pk=self.pk)

        if duplicates.exists():
            # If duplicates found, delete them
            duplicates.delete()

        # Generate a unique slug based on the title
        if not self.slug:
            base_slug = slugify(self.title)
            self.slug = base_slug
            counter = 1

            while NewsPost.objects.filter(slug=self.slug).exists():
                self.slug = f"{base_slug}-{counter}"
                counter += 1

        super().save(*args, **kwargs)
    
    def __str__(self):
        return self.title 