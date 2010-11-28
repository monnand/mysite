from django.http import HttpResponse, HttpResponseRedirect
from django.http import HttpRequest
from django.template.loader import render_to_string
from django.shortcuts import render_to_response
import datetime
import os
import os.path
import re

from accounting.models import PaymentRecord
from accounting.models import SubmissionInfo
from accounting.models import PaymentDefaulterMap
from accounting.forms import PaymentInputForm

comma_splitter = re.compile("\s*,\s*")
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
            defaulters = form.cleaned_data['defaulters']
            defaulters = defaulters.strip()
            defaulters = comma_splitter.split(defaulters)
            now = datetime.datetime.now()
            pr = PaymentRecord(name = name, amount = amount, memo = memo, \
                    is_valid = True, start_time = now)
            pr.save()
            header = request.META['HTTP_HOST']
            agent = request.META['HTTP_USER_AGENT']
            host = request.META['REMOTE_ADDR']
            info = SubmissionInfo(payment = pr, user_agent = agent, \
                    header = header, remote_addr = host, submission_time = now)
            info.save()
            for d in defaulters:
                if d:
                    pdm = PaymentDefaulterMap(payment = pr, defaulter = d)
                    pdm.save()
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

def show_submission_info(request, prid):
    infos = SubmissionInfo.objects.filter(payment__id = prid)
    defaulters = PaymentDefaulterMap.objects.filter(payment__id = prid)
    ds = []
    for d in defaulters:
        ds.append(d.defaulter)
    if ds:
        ds = ", ".join(ds)
    else:
        ds = "All Others"
    content = render_to_string('submissioninfo.html', \
            {'info':infos[0], 'defaulters':ds})
    return render_content('Details', content)
