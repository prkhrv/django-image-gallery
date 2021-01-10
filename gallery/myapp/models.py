from django.db import models
from taggit.managers import TaggableManager

# Create your models here.
class Gallery(models.Model):
    image = models.FileField(upload_to='images/',blank=True)
    tags = TaggableManager()

class Tag(models.Model):
    tag_name = models.CharField(max_length=20,blank=True)

    def __str__(self):
        return self.tag_name