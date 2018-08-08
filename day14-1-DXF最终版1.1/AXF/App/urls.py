from django.conf.urls import url
from .views import *


urlpatterns = [
    url(r'^home/$', home, name='home'),

    url(r'^market/$', market, name='market'),
    url(r'^marketwithparams/(\d+)/(\d+)/(\d+)/$', market_with_params, name='marketwithparams'),

    url(r'^cart/$', cart, name='cart'),
    url(r'^cartadd/$', cart_add, name='cartadd'),
    url(r'^cartnumadd/$', cart_num_add, name='cartnumadd'),
    url(r'^cartnumreduce/$', cart_num_reduce, name='cartnumreduce'),
    url(r'^cartdel/$', cart_del, name='cartdel'),
    url(r'^cartselect/$', cart_select, name='cartselect'),
    url(r'^cartallselect/$', cart_allselect, name='cartallselect'),


    url(r'^mine/$', mine, name='mine'),
    url(r'^register/$', register, name='register'),
    url(r'^registerhandle/$', register_handle, name='registerhandle'),
    url(r'^checkusername/$', check_username, name='checkusername'),
    url(r'^logout/$', logout, name='logout'),
    url(r'^login/$', login, name='login'),
    url(r'^loginhandle/$', login_handle, name='loginhandle'),


    url(r'^order/(\d+)/$', order, name='order'),
    url(r'^orderadd/$', order_add, name='orderadd'),
    url(r'^orderchangestatus/$', order_change_status, name='orderchangestatus'),
    url(r'^orderunpay/$', order_unpay, name='orderunpay'),
    url(r'^orderunreceive/$', order_unreceive, name='orderunreceive'),

]


