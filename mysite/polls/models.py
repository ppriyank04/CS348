from django.db import models
from django.core.validators import MinValueValidator
from decimal import Decimal

class Stock(models.Model):

    STOCK_TYPE_CHOICES = [
        ('dividend', 'Dividend'),
        ('growth', 'Growth'),
        ('value', 'Value'),
        ('other', 'Other'),
    ]
    
    symbol = models.CharField(max_length=10, unique=True)
    company_name = models.CharField(max_length=200)
    stock_type = models.CharField(max_length=50, choices=STOCK_TYPE_CHOICES)
    quantity = models.IntegerField(validators=[MinValueValidator(0)])  # Ensure quantity is not negative
    price = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(Decimal('0.01'))])  # Ensure price is not negative or zero

    class Meta:
        indexes = [
            models.Index(fields=['symbol'], name='symbol_idx'),
            models.Index(fields=['company_name'], name='company_name_idx'),
            # Composite index example
            models.Index(fields=['price'], name='stock_price_idx'),

        ]

    def __str__(self):
        return f"{self.company_name} ({self.symbol})"
