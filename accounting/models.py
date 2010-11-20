from django.db import models

class PaymentRecord(models.Model):
    name = models.CharField(max_length=32)
    amount = models.FloatField()
    memo = models.TextField()
    is_valid = models.BooleanField()
    start_time = models.DateTimeField()
