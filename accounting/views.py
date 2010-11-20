from django.http import HttpResponse, HttpResponseRedirect
from django.http import HttpRequest
from django.template.loader import render_to_string
from django.shortcuts import render_to_response
import datetime
import os
import os.path

from accounting.models import PaymentRecord
from accounting.forms import PaymentInputForm

def add_payment(request):
    form = None
    errmsg = ""
    if request.method == 'POST':
        form = PaymentInputForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            amount = form.cleaned_data['amount']
            memo = form.cleaned_data['memo']
            pr = PaymentRecord(name = name, amount = amount, memo = memo, \
                    is_valid = True, start_time = datetime.datetime.now())
            pr.save()
            return HttpResponse(form.cleaned_data['name'])
#            return HttpResponseRedirect('/hello_world/')
        else:
            return render_to_response('paymentinputform.html', \
                    {'form': form, 'errmsg': errmsg})
    else:
        form = PaymentInputForm()
    return render_to_response('paymentinputform.html', \
            {'form': form, 'errmsg': errmsg})

def show_all_rcd(request):
    rcdlist = PaymentRecord.objects.all()
    return render_to_response('rcdlist.html', \
            {'rcdlist': rcdlist})

