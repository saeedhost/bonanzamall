from django.db import models
from autoslug import AutoSlugField
from tinymce.models import HTMLField
from django.contrib.auth.models import User
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType

class Top_Product(models.Model):
    CHOICES = (
        (1, 'Men Watch'),
        (2, 'Men Smart Watches'),
        (3, 'Men Rings'),
        (4, 'Men Wallet'),
        (5, 'Men Smart Wallet'),
        (6, 'Women Jewelry Sets'),
        (7, 'Women Fashion Watches'),
        (8, 'Women Fashion Rings'),
        (9, 'Women Fashion Necklace'),
        (10, 'Women Fashion Bags'),
        (11, 'Earbuds'),
        (12, 'USB Flash Drive'),
    )
    product_name = models.CharField(max_length=255)
    product_short_description = models.CharField(max_length=255)
    actual_price = models.IntegerField()
    list_price = models.IntegerField()
    percent_off = models.IntegerField()
    main_image_link = models.CharField(max_length=255)
    sub_image_link_2 = models.CharField(max_length=255)
    sub_image_link_3 = models.CharField(max_length=255)
    sub_image_link_4 = models.CharField(max_length=255)
    product_long_description = HTMLField()
    product_specification = HTMLField()
    product_category = models.IntegerField(choices=CHOICES)

    product_quantity = models.IntegerField()
    slug_ref=AutoSlugField(populate_from="product_name",unique=True, null=True, default=None) 

class Special_Offer(models.Model):
    CHOICES = (
        (1, 'Men Watch'),
        (2, 'Men Smart Watches'),
        (3, 'Men Rings'),
        (4, 'Men Wallet'),
        (5, 'Men Smart Wallet'),
        (6, 'Women Jewelry Sets'),
        (7, 'Women Fashion Watches'),
        (8, 'Women Fashion Rings'),
        (9, 'Women Fashion Necklace'),
        (10, 'Women Fashion Bags'),
        (11, 'Earbuds'),
        (12, 'USB Flash Drive'),
    )
    product_name = models.CharField(max_length=255)
    product_short_description = models.CharField(max_length=255)
    actual_price = models.IntegerField()
    list_price = models.IntegerField()
    percent_off = models.IntegerField()
    main_image_link = models.CharField(max_length=255)
    sub_image_link_2 = models.CharField(max_length=255)
    sub_image_link_3 = models.CharField(max_length=255)
    sub_image_link_4 = models.CharField(max_length=255)
    product_long_description = HTMLField()
    product_specification = HTMLField()
    product_category = models.IntegerField(choices=CHOICES)

    product_quantity = models.IntegerField()
    slug_ref=AutoSlugField(populate_from="product_name",unique=True, null=True, default=None) 

class Store_Product(models.Model):
    CHOICES = (
        (1, 'Men Watch'),
        (2, 'Men Smart Watches'),
        (3, 'Men Rings'),
        (4, 'Men Wallet'),
        (5, 'Men Smart Wallet'),
        (6, 'Women Jewelry Sets'),
        (7, 'Women Fashion Watches'),
        (8, 'Women Fashion Rings'),
        (9, 'Women Fashion Necklace'),
        (10, 'Women Fashion Bags'),
        (11, 'Earbuds'),
        (12, 'USB Flash Drive'),
    )
    product_name = models.CharField(max_length=255)
    product_short_description = models.CharField(max_length=255)
    actual_price = models.IntegerField()
    list_price = models.IntegerField()
    percent_off = models.IntegerField()
    main_image_link = models.CharField(max_length=255)
    sub_image_link_2 = models.CharField(max_length=255)
    sub_image_link_3 = models.CharField(max_length=255)
    sub_image_link_4 = models.CharField(max_length=255)
    product_long_description = HTMLField()
    product_specification = HTMLField()
    product_category = models.IntegerField(choices=CHOICES)

    product_quantity = models.IntegerField()
    slug_ref=AutoSlugField(populate_from="product_name",unique=True, null=True, default=None)

class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')
    content = models.TextField()
    image = models.ImageField(upload_to='comment_images/', blank=True, null=True)
    rating = models.PositiveIntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Comment by {self.user.username} on {self.content_object.product_name}"



