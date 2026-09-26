from django.db import models
from django.utils.text import slugify

class Product(models.Model):
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)  # Better than FloatField for currency
    description = models.TextField()
    image = models.ImageField(upload_to="images/")
    slug = models.SlugField(unique=True, blank=True)
    stock = models.IntegerField()
    active = models.BooleanField(default=True)

    def save(self, *args, **kwargs):
        # Generate initial slug if empty
        if not self.slug:
            base_slug = slugify(self.name)
            slug = base_slug
            counter = 1
            
            # Ensure slug uniqueness by appending a counter if a collision occurs
            while Product.objects.filter(slug=slug).exclude(pk=self.pk).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1
                
            self.slug = slug

        # Call the original save() method
        super().save(*args, **kwargs)