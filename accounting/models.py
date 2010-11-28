from django.db import models

class PaymentRecord(models.Model):
    name = models.CharField(max_length=32)
    amount = models.FloatField()
    memo = models.TextField()
    is_valid = models.BooleanField()
    start_time = models.DateTimeField()

class SubmissionInfo(models.Model):
    payment = models.OneToOneField(PaymentRecord, primary_key = True)
    user_agent = models.TextField()
    header = models.TextField()
    remote_addr = models.IPAddressField()
    submission_time = models.DateTimeField()

class PaymentDefaulterMap(models.Model):
    payment = models.ForeignKey(PaymentRecord)
    defaulter = models.TextField()

class PaymentComment(models.Model):
    payment = models.ForeignKey(PaymentRecord)
    name = models.CharField(max_length=32)
    comment = models.TextField()
    time = models.DateTimeField()

