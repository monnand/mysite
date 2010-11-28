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
from accounting.models import PaymentComment
from accounting.models import ShortMessage
from accounting.forms import PaymentInputForm
from accounting.forms import PaymentCommentForm

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
                if d and d != "All Others":
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

def get_recent_messages_on_board(form, redirect, n):
    msgs = []
    if n <= 0:
        msgs = ShortMessage.objects.all()
    else:
        msgs = ShortMessage.objects.all()[0:n]
    ret = render_to_string('messageboard.html', \
            {'form':form, 'comments':msgs, 'url': redirect})

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

def get_defaulters_str(prid):
    defaulters = PaymentDefaulterMap.objects.filter(payment__id = prid)
    ds = []
    for d in defaulters:
        ds.append(d.defaulter)
    if ds:
        ds = ", ".join(ds)
    else:
        ds = "All Others"
    return ds

def show_payment_comment(request, prid):
    defaulters = get_defaulters_str(prid)
    payment = PaymentRecord.objects.filter(id = prid)
    if not payment:
        return HttpResponseRedirect('/vldrcd/')
    payment = payment[0]
    comments = PaymentComment.objects.filter(payment__id = prid)
    form = None
    if request.method == 'POST':
        form = PaymentCommentForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            comment = form.cleaned_data['comment']
            now = datetime.datetime.now()
            c = PaymentComment(payment = payment, name = name, \
                    comment = comment, time = now)
            c.save()
    else:
        form = PaymentCommentForm()
    content = render_to_string('paymentcomments.html', \
            {'rcd': payment, 'defaulters': defaulters, 'comments':comments, \
            'form': form})
    return render_content('Comment', content)

def show_submission_info(request, prid):
    infos = SubmissionInfo.objects.filter(payment__id = prid)
    if not infos:
        return HttpResponseRedirect('/vldrcd/')
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
