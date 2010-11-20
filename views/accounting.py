from django.http import HttpResponse, HttpResponseRedirect
from django.http import HttpRequest
from django.template.loader import render_to_string
import datetime
import os
import os.path

from forms.paymentinput import PaymentInputForm

def add_payment(request):
    if request.method == 'POST':
        form = PaymentInputForm(request.POST)
        if form.is_valid():
            return HttpResponseRedirect('/valid_records/')
    else:
        form = PaymentInputForm()
    return render_to_string('paymentinputform.html', {'form': form,})

