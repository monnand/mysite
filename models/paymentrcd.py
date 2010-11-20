from django.db import models

class PaymentRecord(models.Model):
    name = models.CharField(max_lenght=36)
    amount = models.FloatField()
    memo = models.TextField()
    is_valid = models.BooleanField()
    start_time = models.DateTileField()
