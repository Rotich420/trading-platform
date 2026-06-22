from django.db import models
from django.conf import settings


class Trade(models.Model):
    BUY = 'BUY'
    SELL = 'SELL'
    TRADE_TYPES = [(BUY, 'Buy'), (SELL, 'Sell')]

    PENDING = 'PENDING'
    COMPLETED = 'COMPLETED'
    CANCELLED = 'CANCELLED'
    STATUS_CHOICES = [(PENDING, 'Pending'), (COMPLETED, 'Completed'), (CANCELLED, 'Cancelled')]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='trades')
    symbol = models.CharField(max_length=10)  # e.g. AAPL, BTC
    trade_type = models.CharField(max_length=4, choices=TRADE_TYPES)
    quantity = models.DecimalField(max_digits=15, decimal_places=4)
    price = models.DecimalField(max_digits=15, decimal_places=2)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default=PENDING)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.trade_type} {self.quantity} {self.symbol} @ ${self.price}"

    @property
    def total_value(self):
        return self.quantity * self.price
