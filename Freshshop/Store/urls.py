from django.urls import path,re_path
from Store.views import *

urlpatterns = [
    path('register/',register),
    path('login/',login),
    path('index/',index),
    path('ra/',registerajax),
    path('la/',loginajax),
    path('blank/',blank),
    path('register_store/',register_store),
    path('add_good/',add_good),
    re_path(r'good_list/(?P<state>\w+)',list_good),
    path('goods/',goods),
    path('goods_update/',goods_update),
    path('new/',new),
    re_path(r'goods_set/(?P<state>\w+)',goods_set),
    path('goods_type/',goods_type),
    path('type_delete/',type_delete),
    path('type_add/',type_add),
    path('type/',type),
    re_path(r'type_allgood/(?P<id>\d+)',type_allgood)
]
