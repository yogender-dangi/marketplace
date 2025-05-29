from django.contrib.auth.models import User
from django.db import models
from django.core.exceptions import ValidationError

class Category(models.Model):
    name = models.CharField(max_length=255, unique=True)

    class Meta:
        ordering = ('name',)
        verbose_name_plural = 'Categories'
    
    def clean(self):
        if Category.objects.exclude(pk=self.pk).filter(name__iexact=self.name).exists():
            raise ValidationError({'name': 'A category with this name already exists.'})

    def __str__(self):
        return self.name

class Item(models.Model):
    CONDITION_CHOICES = [
        ('new', 'New'),
        ('used', 'Used'),
        ('refurbished', 'Refurbished'),
    ]

    category = models.ForeignKey(Category, related_name='items', on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    price = models.FloatField()
    image = models.ImageField(upload_to='item_images', blank=True, null=True)
    is_sold = models.BooleanField(default=False)
    created_by = models.ForeignKey(User, related_name='items', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    wishlisted_by = models.ManyToManyField(User, related_name='wishlist', blank=True)
    views = models.IntegerField(default=0)  # Track item views
    condition = models.CharField(max_length=20, choices=CONDITION_CHOICES, default='new')
    
    def __str__(self):
        return self.name

    @property
    def image_url(self):
        if self.image and hasattr(self.image, 'url'):
            return self.image.url
        return '/media/default.jpg'  # This will be our default image