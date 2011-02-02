from django.conf.urls.defaults import *

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    # Example:
    # (r'^mysite/', include('mysite.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # (r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # (r'^admin/', include(admin.site.urls)),
    (r'^$', 'mysite.accounting.views.show_valid_rcd'),
    (r'hello_world/', 'mysite.testcases.hello.read_header'),
    (r'addpay/$', 'mysite.accounting.views.add_payment'),
    (r'allrcd/$', 'mysite.accounting.views.show_all_rcd'),
    (r'vldrcd/$', 'mysite.accounting.views.show_valid_rcd'),
    (r'submissioninfo/(\d+)$', 'mysite.accounting.views.show_submission_info'),
    (r'paymentcomment/(\d+)$', 'mysite.accounting.views.show_payment_comment'),
    (r'delpayment/(\d+)$', 'mysite.accounting.views.del_payment'),
)
