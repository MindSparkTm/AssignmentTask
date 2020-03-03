from django.db import models
from django.utils.translation import ugettext_lazy as _
# Create your models here.

class TimeStampedModel(models.Model):
    """
    An abstract base class model that provides self-
    . fields.
    updating ``created`` and ``modified``
    """
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    class Meta:
        abstract = True
        ordering =['-modified']

class Unit(TimeStampedModel):
    name = models.CharField(max_length=20,verbose_name=_('Unit of Measurement'))

    def __str__(self):
        return u'{}'.format(self.name)

class Item(TimeStampedModel):
    name = models.CharField(verbose_name=_('Name of Item'),max_length=100)
    description = models.TextField(blank=True,null=True)
    quantity = models.DecimalField(max_digits=20, decimal_places=2)
    unit = models.ForeignKey(Unit,on_delete=models.CASCADE)

    def __str__(self):
        return u'{}{}'.format(self.name,self.quantity,self.unit.name)

    def get_absolute_url(self):
        from django.urls import reverse
        return reverse('djangotask:item-detail', args=[str(self.pk)])

    class Meta:
        verbose_name = _('Item Detail')
        verbose_name_plural = _('Item Details')






