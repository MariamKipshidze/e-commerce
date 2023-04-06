import versatileimagefield.fields
from ckeditor_uploader.fields import RichTextUploadingField
from colorfield.fields import ColorField

from django.db import models
from django.db.models import Max
from django.utils.translation import gettext_lazy as _

from e_commerce.utils import unique_slugify


class Product(models.Model):
    category = models.ForeignKey(
        to='Category',
        related_name='products',
        verbose_name=_('Category'),
        null=True,
        on_delete=models.SET_NULL
    )
    collections = models.ManyToManyField(
        to='ProductCollection',
        related_name='products',
        verbose_name=_('Collections'),
        through='ProductCollectionToProduct',
        blank=True,
    )
    title = models.CharField(verbose_name=_('Title'), max_length=255)
    price = models.DecimalField(verbose_name=_("Product Cost"), max_digits=7, decimal_places=2, default=0)
    description = RichTextUploadingField(verbose_name=_("Description"), null=True, blank=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = _('Product')
        verbose_name_plural = _('Products')


class Category(models.Model):
    title = models.CharField(max_length=225, verbose_name=_('Title'))
    slug = models.SlugField(verbose_name=_('Slug'))
    order = models.PositiveIntegerField(default=0, blank=False, null=False)
    is_active = models.BooleanField("Is Active", default=True)
    color = ColorField(default='#FF0000')
    # -- Meta Tags
    meta_title = models.CharField(verbose_name=_('Meta Title'), max_length=60, blank=True, null=True)
    meta_description = models.TextField(verbose_name=_('Meta Description'), max_length=160, blank=True, null=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = _('Category')
        verbose_name_plural = _('Categories')
        ordering = ('order',)


class ProductCollection(models.Model):
    category = models.ForeignKey(
        to='store.Category',
        related_name='collections',
        verbose_name=_('Category'),
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
    )
    title = models.CharField(verbose_name=_('Title'), max_length=255)
    slug = models.SlugField(
        verbose_name=_('Slug'), unique=True, blank=True, null=False, max_length=255,
        help_text=_("This field will be fill automatically, but you can change it")
    )
    image = versatileimagefield.fields.VersatileImageField(
        verbose_name=_("Image"), upload_to='store/collections', blank=True, null=True,
    )
    image_alt_tag = models.CharField(verbose_name=_('Image Alt Tag'), max_length=160, blank=True, null=True)
    description = models.TextField(verbose_name=_('Description'), blank=True, null=True)
    order = models.PositiveIntegerField(verbose_name=_('Order'), default=0, blank=False, null=False)
    # -- Meta Tags
    meta_description = models.TextField(verbose_name=_('Meta Description'), max_length=160, blank=True, null=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            unique_slugify(instance=self, value=self.title)
        super(ProductCollection, self).save(*args, **kwargs)

    class Meta:
        verbose_name = _('Product Collection')
        verbose_name_plural = _('Product Collections')
        ordering = ('order',)


class ProductCollectionToProduct(models.Model):
    product = models.OneToOneField(
        to='store.Product',
        related_name='products_to_collection',
        verbose_name=_('Product'),
        on_delete=models.CASCADE,
    )
    collection = models.ForeignKey(
        to='store.ProductCollection',
        related_name='collection_to_products',
        verbose_name=_('Product Collection'),
        on_delete=models.CASCADE,
    )
    order = models.PositiveIntegerField(verbose_name=_('Order'), default=0, blank=False, null=False)

    def save(self, *args, **kwargs) -> None:
        if not self.order:
            max_order = self.collection.collection_to_products.aggregate(max_order=Max("order")).get("max_order") or 0
            self.order = max_order + 1
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = _('Product Collection To Product')
        verbose_name_plural = _('Product Collections to Products')
        ordering = ('order',)
