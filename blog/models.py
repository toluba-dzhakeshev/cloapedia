from django.db import models
from users.models import Profile


class Category(models.Model):
    COLOR_CHOICES = (
        ('grey', 'grey'),
        ('red', 'red'),
        ('aqua', 'aqua'),
        ('yellow', 'yellow'),
        ('pink', 'pink'),
        ('green', 'green'),
    )

    title = models.CharField(max_length=255)
    color = models.CharField(choices=COLOR_CHOICES, blank=True, null=True, max_length=6)

    class Meta:
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.title


class Post(models.Model):
    category = models.ForeignKey(Category, on_delete=models.SET_NULL,
                                 blank=True, null=True, related_name='posts')
    author = models.ForeignKey(Profile, on_delete=models.SET_NULL,
                               blank=True, null=True, related_name='author_posts')
    title = models.CharField(max_length=255)
    post = models.TextField()
    image = models.ImageField(upload_to='posts', blank=True, null=True)
    rating = models.FloatField(default=0)
    seen_amount = models.PositiveIntegerField(default=0)
    published = models.BooleanField(default=False)
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('-date_created',)

    def __str__(self):
        return self.title
