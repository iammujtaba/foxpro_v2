from django.db import models
from django.core.exceptions import ValidationError
# Create your models here.


class HSN(models.Model):
    code = models.CharField(max_length=10, unique=True)
    gst_percentage = models.DecimalField(max_digits=5, decimal_places=2)
    product_names = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return f"{self.code} - {self.gst_percentage}%"

    class Meta:
        verbose_name = "HSN Code"
        verbose_name_plural = "HSN Codes"


class Item(models.Model):
    item_code = models.CharField(max_length=20, unique=True)
    name = models.CharField(max_length=100)
    quantity = models.PositiveIntegerField(default=0)
    closing_quantity = models.PositiveIntegerField(default=0)
    net_rate = models.DecimalField(max_digits=10, decimal_places=2)
    bill_rate = models.DecimalField(max_digits=10, decimal_places=2)
    purchase_rate = models.DecimalField(max_digits=10, decimal_places=2)
    sgst = models.DecimalField(max_digits=5, decimal_places=2, default=0.0)
    cgst = models.DecimalField(max_digits=5, decimal_places=2, default=0.0)
    igst = models.DecimalField(max_digits=5, decimal_places=2, default=0.0)
    total_gst = models.DecimalField(max_digits=6, decimal_places=2, default=0.0)
    expenses = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)
    profit = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)
    item_sale_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0.0)
    item_purchase_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0.0)
    category = models.CharField(max_length=20, default="z")
    hsn_code = models.ForeignKey(HSN, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f"{self.item_code} - {self.name}"

    @property
    def sale_rate_amount(self):
        return self.quantity * self.net_rate
    

    @property
    def current_quantity(self):
        """Current quantity is the closing_quantity if available, otherwise quantity"""
        return self.closing_quantity if self.closing_quantity > 0 else self.quantity
    
    @property
    def stock_value(self):
        """Calculate stock value as current_quantity * purchase_rate"""
        return self.current_quantity * self.purchase_rate

    def generate_item_code(self):
        return self.category+str(self.pk)

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        self.item_code = self.generate_item_code()
        self.item_sale_amount = self.sale_rate_amount
        self.item_purchase_amount = self.stock_value
        if self.quantity < 0:
            raise ValidationError("Quantity should be greater than 0.")
        return super(Item, self).save(force_insert=force_insert, force_update=force_update, using=using, update_fields=update_fields)

    
