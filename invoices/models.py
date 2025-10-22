from django.db import models
from decimal import Decimal  # Import for explicit Decimal handling

class Invoice(models.Model):
    invoice_number = models.CharField(max_length=50, unique=True)
    date = models.DateField()
    company_name = models.CharField(max_length=100)
    company_address = models.TextField()
    client_name = models.CharField(max_length=100)
    client_address = models.TextField()
    tax_rate = models.DecimalField(max_digits=5, decimal_places=2, default=Decimal('0.10'))  # Use Decimal for default

    def calculate_subtotal(self):
        # Sum returns Decimal automatically, but cast to ensure consistency
        return Decimal(sum(item.quantity * item.price for item in self.items.all()) or 0)

    def calculate_tax(self):
        # Remove float() to avoid Decimal * float error; both are now Decimal
        return self.calculate_subtotal() * self.tax_rate

    def calculate_total(self):
        return self.calculate_subtotal() + self.calculate_tax()

class Item(models.Model):
    invoice = models.ForeignKey(Invoice, related_name='items', on_delete=models.CASCADE)
    description = models.CharField(max_length=200)
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)