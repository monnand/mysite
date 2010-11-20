from django import forms

class PaymentInputForm(forms.Form):
    name = forms.CharField(max_length=32)
    amount = forms.FloatField(min_val=0.00)
    memo = forms.CharField()
