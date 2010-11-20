from django.http import HttpResponse, HttpResponseRedirect
from django.http import HttpRequest
from django.template.loader import render_to_string
from django.shortcuts import render_to_response
import datetime
import os
import os.path

from accounting.models import PaymentRecord
from accounting.forms import PaymentInputForm

def render_content(title, content):
    return render_to_response('accountingmain.html', \
            {'title': title, 'content': content})

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
            return HttpResponseRedirect('/vldrcd/')
        else:
            content = render_to_string('paymentinputform.html', \
                    {'form': form, 'errmsg': errmsg})
            return render_to_response('accountingmain.html', \
                    {'title': 'New Payment Record', 'content': content})
    else:
        form = PaymentInputForm()
    content = render_to_string('paymentinputform.html', \
            {'form': form, 'errmsg': errmsg})
    return render_content('New Payment Record', content)

def show_all_rcd(request):
    rcdlist = PaymentRecord.objects.all()
    content = render_to_string('rcdlist.html', \
            {'rcdlist': rcdlist})
    return render_content('All Records', content)

def show_valid_rcd(request):
    rcdlist = PaymentRecord.objects.filter(is_valid = True)
    content = render_to_string('rcdlist.html', \
            {'rcdlist': rcdlist})
    return render_content('All Records', content)
