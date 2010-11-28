from django import forms

class PaymentInputForm(forms.Form):
    name = forms.CharField(max_length=32)
    amount = forms.FloatField(min_value=-1.00)
    defaulters = forms.CharField(required = False)
    memo = forms.CharField()

class PaymentCommentForm(forms.Form):
    name = forms.CharField(max_length=32)
    comment = forms.CharField(widget=forms.Textarea)
