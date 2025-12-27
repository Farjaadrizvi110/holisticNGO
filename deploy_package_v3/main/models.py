from django.db import models
from froala_editor.fields import FroalaField
from taggit.managers import TaggableManager

class Team(models.Model):
    name = models.CharField(max_length=255)
    designation = models.CharField(max_length=255)
    image = models.ImageField(upload_to='teams/')

    def __str__(self):
        return self.name

class Blog(models.Model):
    title = models.CharField(max_length=255)
    content = FroalaField()
    created_at = models.DateTimeField(auto_now_add=True)
    tags = TaggableManager()
    quote = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to='blogs/')

    def __str__(self):
        return self.title
