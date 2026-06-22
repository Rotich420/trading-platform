from django.db import models
from django.conf import settings


class Transaction(models.Model):

    DEPOSIT = "DEPOSIT"
    WITHDRAWAL = "WITHDRAWAL"

    TYPES = [
        (DEPOSIT, "Deposit"),
        (WITHDRAWAL, "Withdrawal"),
    ]

    PENDING = "PENDING"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"

    STATUSS = [
        (PENDING, "Pending"),
        (COMPLETED, "Completed"),
        (FAILED, "Failed"),
    ]

    MPESA = "MPESA"
    STRIPE = "STRIPE"
    PAYPAL = "PAYPAL"

    PROVIDERS = [
        (MPESA, "M-Pesa"),
        (STRIPE, "Stripe"),
        (PAYPAL, "PayPal"),
    ]

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='transactions'
    )

    transaction_type = models.CharField(
        max_length=20,
        choices=TYPES
    )

    provider = models.CharField(
        max_length=20,
        choices=PROVIDERS,
        blank=True,
        null=True
    )

    amount = models.DecimalField(
        max_digits=15,
        decimal_places=2
    )

    status = models.CharField(
        max_length=20,
        choices=STATUSS,
        default=PENDING
    )

    reference = models.CharField(
        max_length=255,
        blank=True,
        null=True
    )

    phone_number = models.CharField(
        max_length=20,
        blank=True,
        null=True
    )

    callback_data = models.JSONField(
        blank=True,
        null=True
    )

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']