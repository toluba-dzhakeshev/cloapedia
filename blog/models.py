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
    HOT_POS_CHOICES = (
        ('pos1', 'pos1'),
        ('pos2', 'pos2'),
        ('pos3', 'pos3'),
        ('pos4', 'pos4'),
        ('pos5', 'pos5'),
    )
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
    hot_pos = models.CharField(choices=HOT_POS_CHOICES, max_length=4, blank=True, null=True)
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('-date_created',)

    def __str__(self):
        return self.title
