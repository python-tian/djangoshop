from django.urls import path,re_path
from Buyer.views import *
urlpatterns = [
    path('index/',index),
    path('register/',register),
    path('login/',login),
    path('goods_list/',goods_list),
    path('pay_result/',pay_result),
    path('goods/',goods),
    path('base1/',base1),
    path('user/',user),
    re_path(r'cut_delete/(?P<state>\w+)',cut_delete)

]
urlpatterns += [
    path('base/',base),
    path('pay_order/',pay_order)
]