from django.http import HttpResponse, HttpResponseRedirect
from django.http import HttpRequest
from django.template.loader import render_to_string, render_to_response
import datetime
import os
import os.path

from forms.paymentinput import PaymentInputForm

def add_payment(request):
    form = None
    if request.method == 'POST':
        form = PaymentInputForm(request.POST)
        if form.is_valid():
            return HttpResponseRedirect('/valid_records/')
    else:
        form = PaymentInputForm()
    return render_to_response('paymentinputform.html', {'form': form,})

