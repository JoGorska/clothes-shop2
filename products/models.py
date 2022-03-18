from django.db import models


class Category(models.Model):
    """
    categories of products
    """
    class Meta:
        """
        helper class to improve the way categories display in admin
        in plural form
        """
        verbose_name_plural = 'Categories'

    name = models.CharField(max_length=254)
    # friendly_name is optional
    friendly_name = models.CharField(max_length=254, null=True, blank=True)

    def __str__(self):
        return f'{self.name}'

    def get_friendly_name(self):
        """
        returns the name of the category
        """
        return self.friendly_name


class Product(models.Model):
    """
    model for product, each product requirens name, category, price, the rest is optional
    """
    category = models.ForeignKey('Category', null=True, blank=True, on_delete=models.SET_NULL)
    sku = models.CharField(max_length=254, null=True, blank=True)
    name = models.CharField(max_length=254)
    description = models.TextField()
    has_sizes = models.BooleanField(default=False, null=True, blank=True)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    rating = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True)
    image_url = models.URLField(max_length=1024, null=True, blank=True)
    image = models.ImageField(null=True, blank=True)

    def __str__(self):
        return f'{self.name}'
