from django import forms

class PaymentInputForm(forms.Form):
    name = forms.CharField(max_length=32)
    amount = forms.FloatField(min_value=-1.00)
    defaulters = forms.CharField()
    memo = forms.CharField()
